# pbpipeline-helloworld-resources

Example SMRT Link `bundle` extension of Pipeline resources used by smrtflow and pbsmrtpipe in SMRT Link

## Registered Core Resources

- Custom *Tool Contracts* are defined using Tool Contract interface defined in [pbcommand](https://github.com/PacificBiosciences/pbcommand). Examples exes are in `bin`. Then can be emitted to (static) JSON files using  
- Custom *Pipelines* are defined in `custom_pipelines.py` and can be emitted to a (static) JSON form by running `python custom_pipelines.py resolved-pipeline-templates`. 
- Custom Pipeline Template Presets are groupings of task options for a specific pipeline id.

Other custom view rule resources:

- Pipeline Template View Rules
- Report View Rules 

## Requirements and Install

- [pbcommand](https://github.com/PacificBiosciences/pbcommand)
- [pbsmrtpipe](https://github.com/PacificBiosciences/pbsmrtpipe)

See the respective repos for install directions.


## Environment Setup

The registered resources that are loaded by the SMRT Link Services and pbsmrtpipe can be extended by setting environment variables. 

- Pipelines: **PB_PIPELINE_TEMPLATE_DIR**
- Tool Contracts: **PB_TOOL_CONTRACT_DIR**
- Report View Rules: **PB_RULES_REPORT_VIEW_DIR**
- Pipeline View Rules: **PB_RULES_PIPELINE_VIEW_DIR**


See `setup-env.sh` for an example.


For using in SMRT Link install, please not that you must set `export SMRT_PYTHON_PASS_PATH_ENVVARS="YES"` for you custom `PATH` to be retained.