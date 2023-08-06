import tempfile
from contextlib import ExitStack
from queue import PriorityQueue
from typing import Iterator, TypeVar, Iterable

from tqdm import tqdm

from ciff_toolkit.ciff_pb2 import DocRecord, Header, Posting, PostingsList
from ciff_toolkit.read import CiffReader, DEFAULT_CHUNK_SIZE
from ciff_toolkit.write import CiffWriter

TA = TypeVar('TA')


class CiffMerge:
    def __init__(self, writer: CiffWriter, *readers: CiffReader, show_progress: bool = True):
        self.writer = writer
        self.readers = readers
        self.show_progress = show_progress

        # Saves the document IDs per CIFF file, and which IDs they get remapped to
        self.docid_mapping: list[dict[int, int]] = [{} for _ in readers]
        self.num_postings_lists = 0
        self.num_docs = 0

    def perform_merge(self):
        with tempfile.TemporaryFile() as tmp_file:
            tmp_writer = CiffWriter(tmp_file)

            header = self.merge_headers()

            tmp_writer.write_documents(self.merge_documents())
            tmp_writer.write_postings_lists(self.merge_postings_lists())

            header.num_docs = self.num_docs
            header.num_postings_lists = self.num_postings_lists

            self.writer.write_header(header)

            tmp_file.seek(0)
            while data := tmp_file.read(DEFAULT_CHUNK_SIZE):
                self.writer.output.write(data)

    def get_headers_per_ciff(self) -> list[Header]:
        return [reader.header for reader in self.readers]

    def get_postings_lists_per_ciff(self) -> list[Iterator[PostingsList]]:
        if self.show_progress:
            return [
                iter(tqdm(reader.read_postings_lists(), position=origin, desc=f'Postings lists [CIFF {origin}]'))
                for origin, reader in enumerate(self.readers)
            ]
        else:
            return [iter(reader.read_postings_lists()) for reader in self.readers]

    def get_documents_per_ciff(self) -> list[Iterator[DocRecord]]:
        if self.show_progress:
            return [
                iter(tqdm(reader.read_documents(), position=origin, desc=f'Documents [CIFF {origin}]'))
                for origin, reader in enumerate(self.readers)
            ]
        else:
            return [iter(reader.read_documents()) for reader in self.readers]

    def merge_headers(self) -> Header:
        headers = self.get_headers_per_ciff()

        result = Header()

        assert len(set(h.version for h in headers)) == 1
        assert len(set(h.total_postings_lists for h in headers)) == 1
        assert len(set(h.total_docs for h in headers)) == 1
        assert len(set(h.total_terms_in_collection for h in headers)) == 1
        assert len(set(h.average_doclength for h in headers)) == 1
        assert len(set(h.description for h in headers)) == 1

        result.version = headers[0].version
        result.total_postings_lists = headers[0].total_postings_lists
        result.total_docs = headers[0].total_docs
        result.total_terms_in_collection = headers[0].total_terms_in_collection
        result.average_doclength = headers[0].average_doclength
        result.description = headers[0].description

        result.num_docs = sum(h.num_docs for h in headers)

        # TODO: reset this description
        # descriptions = '\n'.join(f' {i + 1}. {h.description}' for i, h in enumerate(headers))
        # result.description = f'This is a combination of {len(headers)} CIFF files:\n\n{descriptions}'

        return result

    def merge_documents(self) -> Iterable[DocRecord]:
        docs_per_ciff = self.get_documents_per_ciff()

        pq: PriorityQueue[tuple[str, tuple[int, DocRecord]]] = PriorityQueue()

        for origin, iterable in enumerate(docs_per_ciff):
            if (doc := next(iterable, None)) is not None:
                pq.put((doc.collection_docid, (origin, doc)))

        # TODO: reconsider whether we want to start from 1 or 0
        new_index = 0

        while not pq.empty():
            _, (origin, doc) = pq.get()

            self.docid_mapping[origin][doc.docid] = new_index
            doc.docid = new_index

            # TODO: We do not wish to output documents with the same collection ID twice
            # if doc.collection_docid != prev_collection_docid:
            #     prev_collection_docid = doc.collection_docid

            yield doc
            self.num_docs += 1

            if (doc := next(docs_per_ciff[origin], None)) is not None:
                pq.put((doc.collection_docid, (origin, doc)))

            new_index += 1

    def merge_postings_lists(self) -> Iterable[PostingsList]:
        postings_lists_per_ciff = self.get_postings_lists_per_ciff()

        pq: PriorityQueue[tuple[str, tuple[int, PostingsList]]] = PriorityQueue()

        for origin, iterable in enumerate(postings_lists_per_ciff):
            if (pl := next(iterable, None)) is not None:
                pq.put((pl.term, (origin, pl)))

        while postings_lists := self.get_top_items(pq):
            result = PostingsList()
            result.term = postings_lists[0][1].term
            # TODO: this will not be as straightforward when relieving the assumption of disjoint document sets
            result.df = sum(pl.df for _, pl in postings_lists)
            result.cf = sum(pl.cf for _, pl in postings_lists)
            result.postings.extend(self.merge_postings({origin: iter(pl.postings) for origin, pl in postings_lists}))

            yield result
            self.num_postings_lists += 1

            for origin, _ in postings_lists:
                if (pl := next(postings_lists_per_ciff[origin], None)) is not None:
                    pq.put((pl.term, (origin, pl)))

    def merge_postings(self, iterables: dict[int, Iterator[Posting]]) -> Iterable[Posting]:
        pq: PriorityQueue[tuple[int, tuple[int, int, Posting]]] = PriorityQueue()

        for origin, iterable in iterables.items():
            if (posting := next(iterable, None)) is not None:
                new_docid = self.docid_mapping[origin][posting.docid]
                pq.put((new_docid, (origin, posting.docid, posting)))

        previous_full_docid = 0
        while not pq.empty():
            full_docid, (origin, previous_docid, posting) = pq.get()

            # D-gap encode the document identifiers
            posting.docid = full_docid - previous_full_docid
            previous_full_docid = full_docid

            yield posting

            if (posting := next(iterables[origin], None)) is not None:
                old_docid = previous_docid + posting.docid
                new_docid = self.docid_mapping[origin][old_docid]
                pq.put((new_docid, (origin, old_docid, posting)))

    @staticmethod
    def get_top_items(pq: PriorityQueue[tuple[str, TA]]) -> list[TA]:
        if pq.empty():
            return []

        first_priority, data = pq.get()
        items = [data]

        while not pq.empty():
            priority, data = pq.get()

            if priority == first_priority:
                items.append(data)
            else:
                pq.put((priority, data))
                break

        return items


def merge_ciff_files(inputs, output, show_progress: bool = True):
    with ExitStack() as stack:
        readers = [stack.enter_context(CiffReader(input_file)) for input_file in inputs]
        writer = stack.enter_context(CiffWriter(output))

        merger = CiffMerge(writer, *readers, show_progress=show_progress)

        merger.perform_merge()
