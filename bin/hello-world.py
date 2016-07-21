#!/usr/bin/env python

"""Simple Example Template for creating a CLI tool

Template from:

https://github.com/PacificBiosciences/pbcommand/blob/master/pbcommand/cli/examples/template_simple.py

"""
import os
import sys
import logging

from pbcommand.validators import validate_file
from pbcommand.utils import setup_log
from pbcommand.cli import get_default_argparser_with_base_opts, pacbio_args_runner

log = logging.getLogger(__name__)

__version__ = "0.1.0"


def get_parser():
    """Define Parser. Use the helper methods in validators to validate input"""
    p = get_default_argparser_with_base_opts(__version__, __doc__)
    f = p.add_argument

    f('path_to_file', type=validate_file, help="Path to File")
    f('output_file', help="Path to output TXT file")
    f('--nrecords', type=int, default=10, help="Number of records to write")

    return p


def run_main(path, output_file, nrecords=10):
    """
    Main function that should be called. Typically this is imported from your
    library code.
    This should NOT reference args.*
    """
    with open(output_file, 'w') as f:
        f.write("Input file was {}".format(path))
        for i in xrange(nrecords):
            f.write("record-{}\n".format(i))

    return 0


def args_runner(args):
    log.info("Raw args {a}".format(a=args))
    return run_main(args.path_to_file, args.output_file, nrecords=args.nrecords)


def main(argv):
    return pacbio_args_runner(argv[1:],
                              get_parser(),
                              args_runner,
                              log,
                              setup_log_func=setup_log)


if __name__ == '__main__':
    sys.exit(main(sys.argv))