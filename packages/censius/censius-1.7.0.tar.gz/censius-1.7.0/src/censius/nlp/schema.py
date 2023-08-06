from censius.nlp import DatasetType, ModelType, UseCase

register_training_valid = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "errorMessage": "Dataset `name` is required and must be a string",
        },
        "file": {
            "type": "string",
            "errorMessage": "Filename `file` is required and must be a string",
        },
        "dataset_type": {
            "type": "string",
            "enum": [DatasetType.TEXT],
            "errorMessage": "Dataset `dataset_type` is required and must be from the list of supported dataset types",
        },
    },
    "required": ["name", "file", "dataset_type"],
}


register_model_valid = {
    "type": "object",
    "properties": {
        "model_name": {
            "type": "string",
            "errorMessage": "Model `model_name` is required and must be a string",
        },
        "model_type": {
            "type": "string",
            "enum": [ModelType.LLM],
            "errorMessage": "ModelType `model_type` is required and must be from the list of supported types",
        },
        "use_case": {
            "type": "string",
            "enum": [UseCase.SUMMARIZATION],
            "errorMessage": "UseCase `use_case` is required and must be from the list of supported use cases",
        },
        "dataset_id": {
            "type": "integer",
            "errorMessage": "Dataset `dataset_id` is required and must be an integer",
        },
    },
    "required": ["model_name", "model_type", "use_case", "dataset_id"],
}


# client.log(
#     prediction_id=predictionId,
#     model_id=modelId,   //
#     input=<DatasetType.TEXT>,
#     referenced_output=<DatasetType.TEXT>
#     prediction=<DatasetType.TEXT>,
#     timestamp=int(round(time.time() * 1000)),
# )


log_valid = {
    "type": "object",
    "properties": {
        "log_id": {
            "type": "string",
            "errorMessage": " `log_id` is required and must be a unique string (at max 16 characters)",
        },
        "model_id": {
            "type": "integer",
            "errorMessage": " `model_id` must be an integer, and is required field",
        },
        "input": {
            "type": "string",
            "errorMessage": " `input` is required field, representing the input to the model",
        },
        "referenced_output": {
            "type": "string",
            "errorMessage": " `referenced_output` is required field, representing the referenced output to the model",
        },
        "prediction": {
            "type": "string",
            "errorMessage": " `prediction` is required field, representing the prediction of the model",
        },
        "timestamp": {
            "type": "integer",
            "errorMessage": " `timestamp` is required field, must be in milliseconds example: 1627958400000",
        },
    },
    "required": ["log_id", "model_id", "referenced_output", "prediction", "timestamp"],
}
