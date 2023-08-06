# CIFF Toolkit

This repository contains a Python toolkit for working with [Common Index File Format (CIFF)](https://github.com/osirrc/ciff/) files.

Specifically, it provides a `CiffReader` and `CiffWriter` for easily reading and writing CIFF files. It also provides a handful of CLI tools, such as merging a CIFF file or dumping its contents.

## Installation

To use the CIFF toolkit, install it from PyPI:

```bash
$ pip install ciff-toolkit
```

## Usage

### Reading

To read a CIFF file, you can use the `CiffReader` class. It returns the posting lists and documents as lazy generators, so operations that need to process large CIFF files do not need to load the entire index into memory.

The `CiffReader` can be used as a context manager, automatically opening files if a path is supplied as a `str` or `pathlib.Path`. 

```python
from ciff_toolkit.read import CiffReader

with CiffReader('./path/to/index.ciff') as reader:
    header = reader.read_header()

    for pl in reader.read_postings_lists():
        print(pl)

    for doc in reader.read_documents():
        print(doc)
```

Alternatively, the `CiffReader` also accepts iterables of bytes instead of file paths. This could be useful if, for instance, the index is in a remote location:

```python
import requests
from ciff_toolkit.read import CiffReader

url = 'https://example.com/remote-index.ciff'
with CiffReader(requests.get(url, stream=True).iter_content(1024)) as reader:
    header = reader.read_header()
    ...
```

### Writing

The `CiffWriter` offers a similar context manager API:

```python
from ciff_toolkit.ciff_pb2 import Header, PostingsList, DocRecord
from ciff_toolkit.write import CiffWriter

header: Header = ...
postings_lists: list[PostingsList] = ...
doc_records: list[DocRecord] = ...

with CiffWriter('./path/to/index.ciff') as writer:
    writer.write_header(header)
    writer.write_postings_lists(postings_lists)
    writer.write_documents(doc_records)
```

### Command Line Interface

A couple of CLI commands are supported:

- `ciff_dump INPUT`

  Dumps the contents of a CIFF file, in order to inspect its contents.
- `ciff_merge INPUT... OUTPUT`

  Merges two or more CIFF files into a single CIFF file. Ensures documents and terms are ordered correctly, and will read and write in a streaming manner (i.e. not read all data into memory at once).

  Note: `ciff_merge` requires that the `DocRecord` messages occur before the `PostingsList` messages in the CIFF file, as it needs to remap the internal document identifiers before merging the posting lists. See `ciff_swap` below for more information on how to achieve that. 
- `ciff_swap --input-order [hpd|hdp] INPUT OUTPUT`

  Swaps the `PostingsList` and `DocRecord` messages in a CIFF file (e.g. in order to prepare for merging). The `--input-order` argument specifies the current format of the CIFF file: `hpd` for header - posting lists - documents, and `hdp` for header - documents - posting lists.
- `ciff_zero_index INPUT OUTPUT`

  Takes a CIFF file with 1-indexed documents, and turns it into 0-indexed documents.

## Development

This project uses [Poetry](https://python-poetry.org/) to manage dependencies, configure the project and publish it to PyPI.

To get started, use Poetry to install all dependencies:

```bash
$ poetry install
```

Then, either activate the virtual environment to execute all Python code in the virtual environment, or prepend every command with poetry run.

```bash
$ poetry shell
(venv) $ ciff_dump index.ciff
```

or:

```bash
$ poetry run ciff_dump index.ciff
```
