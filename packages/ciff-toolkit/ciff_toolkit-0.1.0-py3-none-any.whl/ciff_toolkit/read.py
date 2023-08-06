import gzip
from pathlib import Path
from typing import (IO, Callable, Iterable, Iterator, Optional, Sized, TypeVar,
                    Union)

from google.protobuf.internal.decoder import _DecodeVarint32  # type: ignore
from google.protobuf.message import Message

from ciff_toolkit.ciff_pb2 import DocRecord, Header, PostingsList

MT = TypeVar('MT', bound=Message)
T = TypeVar('T')

DEFAULT_CHUNK_SIZE = 128 * 1024


class SizedIterable(Iterable[T], Sized):
    def __init__(self, it: Iterable[T], length: int):
        self.it = it
        self.length = length

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Iterator[T]:
        yield from self.it


class BufferedReader:
    filename: Optional[Path] = None
    chunk_reader: Optional[Iterator[bytes]] = None
    fp: Optional[IO[bytes]] = None

    def __init__(self, source: Union[str, Path, Iterable[bytes]]) -> None:
        if isinstance(source, (str, Path)):
            self.filename = source
        else:
            self.chunk_reader = iter(source)

        self.buffer = bytearray()

    def read_varint(self) -> int:
        self._fill_buffer(16)

        value, offset = _DecodeVarint32(self.buffer, 0)
        self.buffer = self.buffer[offset:]

        return value

    def read(self, n: int) -> bytes:
        self._fill_buffer(n)

        data = self.buffer[:n]
        self.buffer = self.buffer[n:]

        return bytes(data)

    def _fill_buffer(self, n: int) -> None:
        if self.chunk_reader is None:
            raise ValueError('cannot read from non-existent chunk reader')

        while len(self.buffer) < n:
            try:
                self.buffer += next(self.chunk_reader)
            except StopIteration:
                break

    def _file_chunks(self) -> Iterator[bytes]:
        if self.fp is None:
            raise ValueError('cannot read from non-existent file pointer')

        while data := self.fp.read(DEFAULT_CHUNK_SIZE):
            yield data

    def __enter__(self):
        if self.filename is not None:
            open_fn = gzip.open if self.filename.suffix == '.gz' else open
            self.fp = open_fn(self.filename, 'rb')
            self.chunk_reader = self._file_chunks()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fp is not None:
            self.fp.close()


class MessageReader(BufferedReader):
    def read_message(self, message_type: Callable[[], MT]) -> MT:
        serialized_message = self.read_serialized()

        message = message_type()
        message.ParseFromString(serialized_message)

        return message

    def read_serialized(self) -> bytes:
        message_size = self.read_varint()
        serialized_message = self.read(message_size)

        return serialized_message


class CiffReader(MessageReader):
    def __init__(self, source: Union[str, Path, Iterable[bytes]]):
        super().__init__(source)

        self._header: Optional[Header] = None

    @property
    def header(self) -> Header:
        if self._header is None:
            return self.read_header()

        return self._header

    def read_header(self) -> Header:
        self._header = self.read_message(Header)
        return self._header

    def read_documents(self) -> Iterable[DocRecord]:
        documents = (self.read_message(DocRecord) for _ in range(self.header.num_docs))
        return SizedIterable(documents, self.header.num_docs)

    def read_serialized_documents(self) -> Iterable[bytes]:
        serialized_documents = (self.read_serialized() for _ in range(self.header.num_docs))
        return SizedIterable(serialized_documents, self.header.num_docs)

    def read_postings_lists(self) -> Iterable[PostingsList]:
        postings_lists = (self.read_message(PostingsList) for _ in range(self.header.num_postings_lists))
        return SizedIterable(postings_lists, self.header.num_postings_lists)

    def read_serialized_postings_lists(self) -> Iterable[bytes]:
        serialized_postings_lists = (self.read_serialized() for _ in range(self.header.num_postings_lists))
        return SizedIterable(serialized_postings_lists, self.header.num_postings_lists)
