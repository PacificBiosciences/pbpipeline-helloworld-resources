#!/usr/bin/env python
"""
Example for defining Custom Pipelines
using pipelines to emit a Pipeline XML or ResolvedPipeline Template JSON file
"""
import logging
import sys

from pbsmrtpipe.core import PipelineRegistry
from pbsmrtpipe.cli_custom_pipeline import registry_runner_main


log = logging.getLogger(__name__)


class C(object):
    PT_NAMESPACE = "mk_hello_world"


registry = PipelineRegistry(C.PT_NAMESPACE)


def _example_topts():
    return {"mk_hello_world.task_options.dev_message": "Preset Custom Dev Message from register pipeline",
            "mk_hello_world.task_options.nrecords": 12345}


@registry("mk_test1", "MK Test 1", "0.1.0", task_options=_example_topts())
def to_bindings():
    return [("$entry:e_01", "mk_hello_world.tasks.mk_simple_txt:0")]


@registry("dev_hello_subreadset", "Dev HelloWorld SubreadSet Pipeline", "0.1.0")
def to_bindings():
    # Simple task for starting from a SubreadSet
    return [("$entry:e_01", "mk_hello_world.tasks.hello_world_subreadset:0")]


@registry("mk_test2", "MK Test 2", "0.1.0", tags=("dev", "hello-world"), task_options=_example_topts())
def to_bs():
    """Custom Pipeline Registry for dev hello world tasks"""
    b1 = [('$entry:e_01', 'pbsmrtpipe.tasks.dev_hello_world:0')]

    # Dev tasks that are bundled with pbsmrtpipe
    b2 = [('pbsmrtpipe.tasks.dev_hello_world:0', 'pbsmrtpipe.tasks.dev_hello_worlder:0'),
          ('pbsmrtpipe.tasks.dev_hello_world:0', 'pbsmrtpipe.tasks.dev_hello_garfield:0')]

    b3 = [('pbsmrtpipe.tasks.dev_hello_world:0', 'pbsmrtpipe.tasks.dev_txt_to_fasta:0')]

    return b1 + b2 + b3


@registry("mk_test3", "MK Test 3", "0.1.0", tags=("dev",), task_options=_example_topts())
def to_bs():
    """Custom Pipeline B for testing"""

    # Reuse mk_test_1 pipeline output
    b1 = [("mk_hello_world.pipelines.mk_test1:mk_hello_world.tasks.mk_simple_txt:0", "pbsmrtpipe.tasks.dev_txt_to_fasta:0")]

    b3 = [("pbsmrtpipe.tasks.dev_txt_to_fasta:0", 'pbsmrtpipe.tasks.dev_filter_fasta:0')]
    return b1 + b3


if __name__ == '__main__':
    sys.exit(registry_runner_main(registry)(argv=sys.argv))
