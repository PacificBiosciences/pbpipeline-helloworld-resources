# pbpipeline-helloworld-resources

Example SMRT Link `bundle` extension of Pipeline resources used by smrtflow and pbsmrtpipe in SMRT Link.

## Registered Core Resources

- Custom *Tool Contracts* are defined using Tool Contract interface defined in [pbcommand](https://github.com/PacificBiosciences/pbcommand). Examples exes are in `bin`. Then can be emitted to (static) JSON files using `$EXE --emit-tool-contract` or `$EXE emit-tool-contracts` if using the `registry` model.  
- Custom *Pipelines* are defined in `custom_pipelines.py` and can be emitted to a (static) JSON form by running `python custom_pipelines.py resolved-pipeline-templates`. 
- Custom *Pipeline Template Presets* are groupings of task options for a specific pipeline id.
- Custom *Chunk Operators* are XML mappings of how a task is scatter/gathered. See the [pbsmrtpipe docs](pbsmrtpipe.readthedocs.org) for details on the Chunking Framework

Other custom view rules and resources:

- Pipeline Template View Rules
- Report View Rules

## Requirements and Install

- [pbcommand](https://github.com/PacificBiosciences/pbcommand)
- [pbsmrtpipe](https://github.com/PacificBiosciences/pbsmrtpipe)

See the respective repos for install directions.


## Defining Custom Tool Contracts (i.e.,Tasks) and Pipelines

### Tool Contracts

Custom tasks can be defined using the PacBio Tool Contract interface. See [pbcommand](https://github.com/PacificBiosciences/pbcommand) repo for examples and the [pbcommand docs](http://pbcommand.readthedocs.io/)for more details.

Examples tasks are provided in `bin`, specifically, `hello-registry.py`. This is an example of the `quick` interface to register several tasks using a subparser-esque model. 

The static tool contract JSON files can be emitted using `bin/hello-registry.py emit-tool-contracts -o /path/to/output/tool-contracts`


### Defining Pipelines


Pipelines can be defined programmatically using python to encode the edges in the graph using a simple model using `bindings` (edges in graph).
 

Several example pipelines are defined in `custom_pipelines.py`. The static resolved pipeline templates can be emitted using `python custom_pipelines.py /path/to/resolved-pipeline-templates` (Note this requires setting up the ENV correctly. See the makefile targets `emit-pipelines` for details. This will emit static JSON files that can be loaded by both `pbsmrtpipe` and `SMRT Link Analysis Services`.


Please see [pbsmrtpipe docs]([pbsmrtpipe](pbsmrtpipe.readthedocs.org)) for more detail on pipeline creation and pipeline bindings.


# Environment Setup

The registered resources that are loaded by the SMRT Link Services and pbsmrtpipe can be extended by setting environment variables.
 
- Pipelines: **PB_PIPELINE_TEMPLATE_DIR**
- Tool Contracts (JSON files in dir): **PB_TOOL_CONTRACT_DIR**
- Report View Rules (JSON files) in dir: **PB_RULES_REPORT_VIEW_DIR**
- Pipeline View Rules (XML files in dir): **PB_RULES_PIPELINE_VIEW_DIR**
- Chunk Operators (XML files in dir): **PB_CHUNK_OPERATOR_DIR**

See `setup-env.sh` for an explicit example; this can serve as a template
for other similar customizations (i.e. by setting `PROJ_DIR` differently).

## Environment Setup for Commandline (from pbsmrtpipe)

Before running the `pbsmrtpipe` exe to run a pipeline execution, run the `setup-env.sh` to set the necessary ENV variables. Once these are set you pipelines and tool contracts can accessible by showing the registered resources by running `pbsmrtpipe show-templates` and `pbsmrtpipe show-tasks`, respectively.

Note, for using in `pbsmrtpipe` from a SMRT Link install you *must* set `export SMRT_PYTHON_PASS_PATH_ENVVARS="YES"` for your custom `PATH` to be retained.

## Environment Setup for SMRT Link Services and UI

For extending an official SMRT Link install and to use your custom pipelines within the SMRT Link UI, you must do the following.

- shutdown the SMRT Link services
- setup the ENV to source your custom `setup-env.sh` which will enable both the SMRT Link Services and pbsmrtpipe to be aware of these resources
- restart the SMRT Link services

Verification that your custom pipelines have been successfully registered can be performed by using this call the SL services.

`curl http://<SL_HOST>:<SL_PORT>/secondary-analysis/resolved-pipeline-templates`

Or explicitly look for a specific pipeline by id (`CUSTOM_PIPELINE_ID`)

`curl http://<SL_HOST>:<SL_PORT>/secondary-analysis/resolved-pipeline-templates/<CUSTOM_PIPELINE_ID>`


## Testing Pipelines

The recommended model is to create a testkit job using a testkit.cfg file that references a small input dataset types. This intergration test framework will help debug pipeline and tool contracts from the *both* the commandline as well as from the services.

Example testkit jobs are in `testkit-data`

From the commandline within your the directory that contains the testkit.cfg (e.g., dev_hello_subreadset_01)

`pbtestkit-runner testkit.cfg`

This will run `pbsmrtpipe` and to core/basic validation on the job output. See `--help` for more details.

For running all the testkit jobs in `testkit-data`:

`pbtestkit-multirunner testkit-data/testkit.fofn`


Similarly, testkit jobs can be run from the SMRT Link Services.
 
`pbtestkit-service-runner testkit.cfg --host=my-host --port=8081 --debug`

Note, this usecase is specifically for PacBio DataSet driven pipelines (i.e., pipelines driven from a SubreadSet, ReferenceSet, ...) and is *not* general to any pipeline.
 
Run all the service runnable teskit jobs in `testkit-data`:
 
`pbtestkit-service-multirunner testk-data/services-testkit.fofn --host=my-host --port=8081 --debug`


