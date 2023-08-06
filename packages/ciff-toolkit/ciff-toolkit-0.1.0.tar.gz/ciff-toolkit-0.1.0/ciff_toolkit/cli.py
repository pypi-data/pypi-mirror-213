from argparse import ArgumentParser
from pathlib import Path

from ciff_toolkit.merge import merge_ciff_files
from ciff_toolkit.util import (ciff_swap_docrecords_and_postingslists,
                               ciff_swap_postingslists_and_docrecords,
                               ciff_to_zero_indexed_docids, dump_ciff)


def merge():
    parser = ArgumentParser(description='Merge CIFF files into a joined CIFF file.')
    parser.add_argument('inputs', help='Input CIFF files that should be merged', nargs='+', type=Path)
    parser.add_argument('output', help='The destination of the merged CIFF file', type=Path)

    args = parser.parse_args()

    merge_ciff_files(args.inputs, args.output)


def swap():
    parser = ArgumentParser(description='Swap records within a CIFF file.')
    parser.add_argument('input', help='Input CIFF file, of which the records should be swapped', type=Path)
    parser.add_argument('output', help='The destination of the new CIFF file', type=Path)
    parser.add_argument('-o', '--input-order', choices=['hpd', 'hdp'], default='hpd',
                        help='The order of records in the input CIFF file. Options: '
                             '"hpd" (default) for header - posting lists - documents, and '
                             '"hdp" for header - documents - posting lists')

    args = parser.parse_args()

    if args.input_order == 'hpd':
        ciff_swap_postingslists_and_docrecords(args.input, args.output)
    elif args.input_order == 'hdp':
        ciff_swap_docrecords_and_postingslists(args.input, args.output)


def zero_index():
    parser = ArgumentParser(description='Transform 1-indexed docids in a CIFF file to 0-indexed docids.')
    parser.add_argument('input', help='Input CIFF file, of which the docids should be adjusted', type=Path)
    parser.add_argument('output', help='The destination of the new CIFF file', type=Path)

    args = parser.parse_args()

    ciff_to_zero_indexed_docids(args.input, args.output)


def dump():
    parser = ArgumentParser(description='Dump the contents of a CIFF file.')
    parser.add_argument('input', help='Input CIFF file', type=Path)

    args = parser.parse_args()

    dump_ciff(args.input)
