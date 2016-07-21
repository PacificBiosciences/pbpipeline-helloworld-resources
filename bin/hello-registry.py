#!/usr/bin/env python
import sys
import logging
import os
import shutil
import time
import random

from pbcommand.cli import registry_builder, registry_runner
from pbcommand.pb_io.report import fofn_to_report
from pbcommand.models import FileTypes, SymbolTypes, ResourceTypes

from pbcore.io import (readFofn, ReferenceSet, FastqReader, FastaWriter,
                       FastaRecord, FastaReader)

from pbsmrtpipe.mock import write_random_fasta_records
import pbsmrtpipe.schema_opt_utils as OP
from pbsmrtpipe.tools.dev import (subread_dataset_report,
                                  run_random_fofn,
                                  run_reference_dataset_report,
                                  run_fasta_report)

log = logging.getLogger(__name__)

TOOL_NAMESPACE = 'mk_hello_world'
DRIVER_BASE = "hello-registry.py "

registry = registry_builder(TOOL_NAMESPACE, DRIVER_BASE)


def _to_opt_id(name):
    return ".".join([TOOL_NAMESPACE, 'task_options', name])


def write_report_and_log(report, output_file):
    report.write_json(output_file)
    log.debug("Wrote report {r} to {o}".format(r=report, o=output_file))
    return True


def _fastq_to_fasta(fastq_path, fasta_path):
    """Convert a fastq file to  fasta file"""
    with FastqReader(fastq_path) as r:
        with FastaWriter(fasta_path) as w:
            for fastq_record in r:
                fasta_record = FastaRecord(fastq_record.name, fastq_record.sequence)
                w.writeRecord(fasta_record)

    log.info("Completed converting {q} to {f}".format(q=fastq_path, f=fasta_path))
    return 0


def run_fasta_filter(fasta_in, fasta_out, min_seq_length):
    with FastaWriter(fasta_out) as w:
        with FastaReader(fasta_in) as r:
            for record in r:
                if len(record.sequence) > min_seq_length:
                    w.writeRecord(record)

    return 0


def _get_opts():
    oid = OP.to_opt_id('dev.hello_message')
    return {oid: OP.to_option_schema(oid, "string", 'Hello Message', "Hello Message for dev Task.", "Default Message")}


def run_main_dev_hello_world(input_file, output_file):
    with open(input_file, 'r') as f:
        with open(output_file, 'w') as w:
            w.write(f.readline())
    return 0


@registry("dev_hello_world", '0.1.0', FileTypes.TXT, FileTypes.TXT, is_distributed=False, options=dict(dev_message="Hello Dev message"))
def run_rtc(rtc):
    return run_main_dev_hello_world(rtc.task.input_files[0], rtc.task.output_files[0])


@registry("dev_fastq_to_fasta", "0.1.0", FileTypes.FASTQ, FileTypes.FASTA, is_distributed=False)
def run_rtc(rtc):
    return _fastq_to_fasta(rtc.task.input_files[0], rtc.task.output_files[0])


@registry("dev_fasta", "0.2.1", FileTypes.TXT, FileTypes.FASTA, is_distributed=False,
          options=dict(max_nrecords=1000))
def run_rtc(rtc):
    max_records = rtc.tasks.options[_to_opt_id("alpha")]
    return write_random_fasta_records(rtc.task.output_files[0], max_records)


@registry("dev_tc_fasta_report", "0.1.1", FileTypes.FASTA, FileTypes.REPORT, is_distributed=False)
def run_rtc(rtc):
    return run_fasta_report(rtc.task.input_files[0], rtc.task.output_files[0])


@registry("dev_filter_fasta", "0.1.1", FileTypes.FASTA, FileTypes.FASTA, is_distributed=False,
          options=dict(dev_fasta_min_length=50))
def run_rtc(rtc):
    min_seq_length = rtc.task.options[_to_opt_id("dev_fasta_min_length")]
    # this is for testing failures
    if min_seq_length < 0:
        raise ValueError("Invalid min seq length {m}".format(m=min_seq_length))
    return run_fasta_filter(rtc.task.input_files[0], rtc.task.output_files[0], min_seq_length)


@registry("rset_to_txt", "0.1.0", FileTypes.DS_REF, FileTypes.TXT, is_distributed=False)
def run_rtc(rtc):
    """Dev Task for testing pipelines. Generates a Txt file"""

    with open(rtc.task.output_files[0], 'w') as f:
        f.write("Dev Mock converting ReferenceSet {}\n".format(rtc.task.input_files[0]))
        f.write("to text file {}".format(rtc.task.output_files[0]))

    return 0


if __name__ == '__main__':
    sys.exit(registry_runner(registry, sys.argv[1:]))