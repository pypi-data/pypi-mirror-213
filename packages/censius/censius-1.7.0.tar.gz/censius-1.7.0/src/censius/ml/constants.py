from censius.endpoint import CENSIUS_ENDPOINT


GATEWAY_URL = f"{CENSIUS_ENDPOINT}/api/sdkapi"

## The below 2 urls will be deprecated
REGISTER_MODEL_URL = lambda project_id: f"{GATEWAY_URL}/{project_id}/res/registermodel/frd/models/"
REGISTER_NEW_MODEL_VERSION = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/registermodelversion/frd/models/model_version"
)
PROCESS_MODEL_URL = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/processmodel/frd/models/schema-updation"
)

# Models
REGISTER_MODEL_V2_URL = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/registermodelv2/frd/models/v2"
)
REGISTER_NEW_MODEL_VERSION_V2_URL = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/registermodelversionv2/frd/models/v2/model_version"
)
ADD_MODEL_ITERATION = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/additeration/frd/models/addModelIteration"
)

# Logs
LOG_URL = lambda project_id: f"{GATEWAY_URL}/{project_id}/res/postlogv2/frd/api/v2/logs"
UPDATE_ACTUAL_URL = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/updateactualv2/frd/api/v2/update_actuals"
)
BULK_LOG_DATATYPE_VALIDATION_URL = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/bulklogvalidate/frd/v1/logs/validate_bulk_datatype"
)
BULK_LOG_URL = lambda project_id: f"{GATEWAY_URL}/{project_id}/res/bulklog/frd/v1/logs/bulk_logs"
LOG_EXPLAINATIONS_URL = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/explainv2/frd/api/v2/insert_explainations"
)
BULK_EXPLAINATIONS_URL = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/bulkexplain/frd/v1/explainations/bulk_explainations"
)

# Dataset
REGISTER_DATASET_URL = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/registerdataset/frd/api/v1/validate_insert_dataset"
)

# Project


# General constants
BULK_CHUNK_SIZE = 2000
GENERAL_TIMEOUT = 10
BASE_MILLISECONDS_2000 = 946684800000
CEIL_MILLISECONDS_2100 = 4102444800000
