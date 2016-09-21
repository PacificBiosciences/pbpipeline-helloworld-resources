export PROJ_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PB_PIPELINE_TEMPLATE_DIR=${PROJ_DIR}/resolved-pipeline-templates
export PB_TOOL_CONTRACT_DIR=${PROJ_DIR}/tool-contracts

# View Rules
export PB_RULES_REPORT_VIEW_DIR=${PROJ_DIR}/rules-report-view
export PB_RULES_PIPELINE_VIEW_DIR=${PROJ_DIR}/rules-pipeline-template-view

# Extend the PATH to include our custom exe(s)
export PATH=${PROJ_DIR}/bin:$PATH

# For use in a SMRT Link install, Setting export SMRT_PYTHON_PASS_PATH_ENVVARS="YES"
# Will allow your value of $PATH to be used (however, it will be prepended/modified)