# pbpipeline-helloworld-resources

Example SMRT Link `bundle` extension of Pipeline resources used by smrtflow and pbsmrtpipe in SMRT Link

## Registered Core Resources

- Custom *Tool Contracts* are defined using Tool Contract interface defined in [pbcommand](https://github.com/PacificBiosciences/pbcommand). Examples exes are in `bin`. Then can be emitted to (static) JSON files using `$EXE --emit-tool-contract`. 
- Custom *Pipelines* are defined in `custom_pipelines.py` and can be emitted to a (static) JSON form by running `python custom_pipelines.py resolved-pipeline-templates`. 
- Custom Pipeline Template Presets are groupings of task options for a specific pipeline id.

Other custom view rule resources:

- Pipeline Template View Rules
- Report View Rules 

## Requirements and Install

- [pbcommand](https://github.com/PacificBiosciences/pbcommand)
- [pbsmrtpipe](https://github.com/PacificBiosciences/pbsmrtpipe)

See the respective repos for install directions.


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

From the commandline within your the directory that contains the testkit.cfg

`pbtestkit-runner testkit.cfg`

This will run `pbsmrtpipe` and to core/basic validation on the job output. See `--help` for more details.

Similarly, testkit jobs can be run from the SMRT Link Services.
 
`pbtestkit-service-runner testkit.cfg --host=my-host --port=8081 --debug`

Note, this usecase is specifically for PacBio DataSet driven pipelines (i.e., pipelines driven from a SubreadSet, ReferenceSet, ...) and is *not* general to any pipeline. 


