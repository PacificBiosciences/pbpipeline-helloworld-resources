#!/usr/bin/env python
import sys
import logging

from pbcommand.cli import registry_builder, registry_runner
from pbcommand.engine import run_cmd
from pbcommand.models import FileTypes


log = logging.getLogger(__name__)

TOOL_NAMESPACE = 'mk_hello_world'
DRIVER_BASE = "hello-registry "

registry = registry_builder(TOOL_NAMESPACE, DRIVER_BASE)


def _to_opt_id(name):
    return ".".join([TOOL_NAMESPACE, 'task_options', name])


@registry("mk_simple_txt", "0.1.0", FileTypes.TXT, FileTypes.TXT, is_distributed=False)
def run_rtc(rtc):
    """Dev Task for testing pipelines. Generates a Txt file"""

    with open(rtc.task.output_files[0], 'w') as f:
        f.write("Input File {}\n".format(rtc.task.input_files[0]))
        f.write("to text file {}".format(rtc.task.output_files[0]))

    return 0


@registry("mk_simple_txt", "0.1.0", FileTypes.TXT, FileTypes.TXT, is_distributed=False, options=dict(nrecords=21))
def run_rtc(rtc):
    """Dev Task for calling a subprocess exe. In this case it's python"""

    nrecords = rtc.task.options[_to_opt_id("nrecords")]
    _d = dict(i=rtc.task.input_files[0], o=rtc.task.output_files[0], r=nrecords)
    exe = "hello-world.py {i} {p} --nrecords {r}".format(**_d)
    result = run_cmd(exe, sys.stdout, sys.stderr)
    log.info("Completed running {e} Result {r}".format(e=exe, r=result))
    return result


if __name__ == '__main__':
    sys.exit(registry_runner(registry, sys.argv[1:]))