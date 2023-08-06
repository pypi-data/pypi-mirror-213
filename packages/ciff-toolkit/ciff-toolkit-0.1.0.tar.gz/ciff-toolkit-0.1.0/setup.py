# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ciff_toolkit']

package_data = \
{'': ['*'], 'ciff_toolkit': ['protos/*']}

install_requires = \
['protobuf>=4.21.12,<5.0.0', 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['ciff_dump = ciff_toolkit.cli:dump',
                     'ciff_merge = ciff_toolkit.cli:merge',
                     'ciff_swap = ciff_toolkit.cli:swap',
                     'ciff_zero_index = ciff_toolkit.cli:zero_index']}

setup_kwargs = {
    'name': 'ciff-toolkit',
    'version': '0.1.0',
    'description': 'Toolkit for working with Common Index File Format (CIFF) files.',
    'long_description': "# CIFF Toolkit\n\nThis repository contains a Python toolkit for working with [Common Index File Format (CIFF)](https://github.com/osirrc/ciff/) files.\n\nSpecifically, it provides a `CiffReader` and `CiffWriter` for easily reading and writing CIFF files. It also provides a handful of CLI tools, such as merging a CIFF file or dumping its contents.\n\n## Installation\n\nTo use the CIFF toolkit, install it from PyPI:\n\n```bash\n$ pip install ciff-toolkit\n```\n\n## Usage\n\n### Reading\n\nTo read a CIFF file, you can use the `CiffReader` class. It returns the posting lists and documents as lazy generators, so operations that need to process large CIFF files do not need to load the entire index into memory.\n\nThe `CiffReader` can be used as a context manager, automatically opening files if a path is supplied as a `str` or `pathlib.Path`. \n\n```python\nfrom ciff_toolkit.read import CiffReader\n\nwith CiffReader('./path/to/index.ciff') as reader:\n    header = reader.read_header()\n\n    for pl in reader.read_postings_lists():\n        print(pl)\n\n    for doc in reader.read_documents():\n        print(doc)\n```\n\nAlternatively, the `CiffReader` also accepts iterables of bytes instead of file paths. This could be useful if, for instance, the index is in a remote location:\n\n```python\nimport requests\nfrom ciff_toolkit.read import CiffReader\n\nurl = 'https://example.com/remote-index.ciff'\nwith CiffReader(requests.get(url, stream=True).iter_content(1024)) as reader:\n    header = reader.read_header()\n    ...\n```\n\n### Writing\n\nThe `CiffWriter` offers a similar context manager API:\n\n```python\nfrom ciff_toolkit.ciff_pb2 import Header, PostingsList, DocRecord\nfrom ciff_toolkit.write import CiffWriter\n\nheader: Header = ...\npostings_lists: list[PostingsList] = ...\ndoc_records: list[DocRecord] = ...\n\nwith CiffWriter('./path/to/index.ciff') as writer:\n    writer.write_header(header)\n    writer.write_postings_lists(postings_lists)\n    writer.write_documents(doc_records)\n```\n\n### Command Line Interface\n\nA couple of CLI commands are supported:\n\n- `ciff_dump INPUT`\n\n  Dumps the contents of a CIFF file, in order to inspect its contents.\n- `ciff_merge INPUT... OUTPUT`\n\n  Merges two or more CIFF files into a single CIFF file. Ensures documents and terms are ordered correctly, and will read and write in a streaming manner (i.e. not read all data into memory at once).\n\n  Note: `ciff_merge` requires that the `DocRecord` messages occur before the `PostingsList` messages in the CIFF file, as it needs to remap the internal document identifiers before merging the posting lists. See `ciff_swap` below for more information on how to achieve that. \n- `ciff_swap --input-order [hpd|hdp] INPUT OUTPUT`\n\n  Swaps the `PostingsList` and `DocRecord` messages in a CIFF file (e.g. in order to prepare for merging). The `--input-order` argument specifies the current format of the CIFF file: `hpd` for header - posting lists - documents, and `hdp` for header - documents - posting lists.\n- `ciff_zero_index INPUT OUTPUT`\n\n  Takes a CIFF file with 1-indexed documents, and turns it into 0-indexed documents.\n\n## Development\n\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies, configure the project and publish it to PyPI.\n\nTo get started, use Poetry to install all dependencies:\n\n```bash\n$ poetry install\n```\n\nThen, either activate the virtual environment to execute all Python code in the virtual environment, or prepend every command with poetry run.\n\n```bash\n$ poetry shell\n(venv) $ ciff_dump index.ciff\n```\n\nor:\n\n```bash\n$ poetry run ciff_dump index.ciff\n```\n",
    'author': 'Gijs Hendriksen',
    'author_email': 'g.hendriksen@cs.ru.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://opencode.it4i.eu/openwebsearcheu-public/ciff-toolkit/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
