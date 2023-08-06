import tempfile
from pathlib import Path
from typing import Iterable

from ciff_toolkit.read import CiffReader, DEFAULT_CHUNK_SIZE
from ciff_toolkit.write import CiffWriter, MessageWriter


def dump_ciff(file: Path):
    with CiffReader(file) as reader:
        print(reader.header)

        for pl in reader.read_postings_lists():
            print(f'{pl.term}\tdf: {pl.df}\tcf: {pl.cf}')

        for doc in reader.read_documents():
            print(f'Doc {doc.docid} ({doc.collection_docid}), length={doc.doclength}')


def _swap_messages(first_messages: Iterable[bytes], second_messages: Iterable[bytes],
                   writer: MessageWriter):
    with tempfile.TemporaryFile() as tmp_file, MessageWriter(tmp_file) as tmp_writer:
        for message in first_messages:
            tmp_writer.write_serialized(message)

        for message in second_messages:
            writer.write_serialized(message)

        tmp_file.seek(0)
        while data := tmp_file.read(DEFAULT_CHUNK_SIZE):
            writer.write(data)


def ciff_swap_docrecords_and_postingslists(file_in: Path, file_out: Path):
    with CiffReader(file_in) as reader, CiffWriter(file_out) as writer:
        writer.write_header(reader.read_header())
        _swap_messages(reader.read_serialized_documents(), reader.read_serialized_postings_lists(), writer)


def ciff_swap_postingslists_and_docrecords(file_in: Path, file_out: Path):
    with CiffReader(file_in) as reader, CiffWriter(file_out) as writer:
        writer.write_header(reader.read_header())
        _swap_messages(reader.read_serialized_postings_lists(), reader.read_serialized_documents(), writer)


def ciff_to_zero_indexed_docids(file_in: Path, file_out: Path):
    with CiffReader(file_in) as reader, CiffWriter(file_out) as writer:
        writer.write_header(reader.read_header())

        for pl in reader.read_postings_lists():
            pl.postings[0].docid -= 1
            writer.write_message(pl)

        for doc in reader.read_documents():
            doc.docid -= 1
            writer.write_message(doc)
