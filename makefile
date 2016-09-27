PROJ_DIR := $(abspath $(lastword $(MAKEFILE_LIST)))

emit-pipelines:
	# this needs to be unset to avoid loading the current custom pipelines. 
	# Re-emitting the pipelines willl overwrite existing ones.
	unset PB_PIPELINE_TEMPLATE_DIR && python custom_pipelines.py --log-level=INFO resolved-pipeline-templates

emit-tool-contracts:
	bin/hello-registry.py emit-tool-contracts -o tool-contracts
	bin/simple-registry.py emit-tool-contracts -o tool-contracts

emit: emit-pipelines emit-tool-contracts

show-pipelines:
	pbsmrtpipe show-templates

show-tasks:
	pbsmrtpipe show-tasks

test-dev:
	/bin/bash -c "source setup-env.sh && cd testkit-data && pbtestkit-multirunner --debug --nworkers 8 testkit.fofn && cd -"

run-testkit: test-dev

test-pipelines:
	nosetests --verbose pbsmrtpipe.tests.test_pb_pipelines_sanity

test-loader:
	python -c "import pbsmrtpipe.loader as L; L.load_all()"

test-contracts:
	python -c "import pbsmrtpipe.loader as L; L.load_all()"

test-chunk-operators:
	python -c "import pbsmrtpipe.loader as L; L.load_and_validate_chunk_operators()"

test-sanity: test-contracts test-pipelines test-chunk-operators test-loader 

clean:
	find . -name "*.pyc" | xargs rm -rf
	find . -name "job_output" | xargs rm -rf
	find . -name "0.std*" -delete
