import requests
import json
import pandas as pd
from .constants import (
    LLM_REGISTER_DATASET_URL,
    LLM_REGISTER_LOGS,
    LLM_REGISTER_MODEL_URL,
    BULK_CHUNK_SIZE,
)
from censius.helper import validate_input
from censius.CensiusParent import CensiusParent
from censius.nlp.schema import register_training_valid, register_model_valid, log_valid


class CensiusClient(CensiusParent):
    def register_dataset(self, *args, **kwargs):
        error_flag, msg = validate_input(kwargs, register_training_valid)
        if error_flag:
            return msg

        file_path = kwargs["file"]
        dataset_type = kwargs["dataset_type"]
        dataset_name = kwargs["name"]
        project_id = self.project_id
        usecase = "llm"
        dataset_version = 1
        modality = "tabular"

        reader = pd.read_csv(file_path, chunksize=BULK_CHUNK_SIZE)
        num_chunks = sum(1 for _ in reader)
        reader = pd.read_csv(file_path, chunksize=BULK_CHUNK_SIZE)
        total_rows = num_chunks * BULK_CHUNK_SIZE
        dataset_id = None
        for i, chunk in enumerate(reader):
            json_data = {}
            json_data["training_data"] = json.loads(chunk.to_json(orient="records"))
            json_data["is_last_chunk"] = True if (i + 1) == num_chunks else False
            json_data["training_datatype"] = dataset_type
            json_data["dataset_name"] = dataset_name
            json_data["usecase"] = usecase
            json_data["project_id"] = project_id
            json_data["dataset_version"] = dataset_version
            json_data["modality"] = modality
            json_data["size"] = total_rows

            if dataset_id is None:
                url = LLM_REGISTER_DATASET_URL(self.project_id)
                response = requests.request(
                    "POST",
                    url,
                    headers=self.get_headers(),
                    data=json.dumps(json_data),
                )

                if response.status_code == 200:
                    dataset_id = response.json()["details"]["datasetId"]
                else:
                    return {"status": "error", "details": "failed to register dataset"}
            else:
                json_data["dataset_id"] = dataset_id
                url = LLM_REGISTER_DATASET_URL(
                    project_id=self.project_id
                )
                requests.request(
                    "POST",
                    url,
                    headers=self.get_headers(),
                    data=json.dumps(json_data),
                )

        return {
            "status": "success",
            "details": "registeration completed successfully",
            "dataset_id": dataset_id,
        }

    def register_model(self, *args, **kwargs):
        error_flag, msg = validate_input(kwargs, register_model_valid)
        if error_flag:
            return msg

        model_data = {
            "model_name": kwargs["model_name"],
            "model_type": kwargs["model_type"],
            "use_case": kwargs["use_case"],
        }
        dataset_id = kwargs["dataset_id"]
        parent_model_id = None

        url = LLM_REGISTER_MODEL_URL(self.project_id, dataset_id)
        model_data["parent_model_id"] = parent_model_id
        payload = json.dumps(model_data)
        response = requests.request("POST", url, headers=self.get_headers(), data=payload)
        return response.json()

    def log(self, *args, **kwargs):
        error_flag, msg = validate_input(kwargs, log_valid)
        if error_flag:
            return msg

        input_data = "random string"
        log_id = kwargs["log_id"]
        model_id = kwargs["model_id"]
        prediction = kwargs["prediction"]
        referenced_output = kwargs["referenced_output"]
        timestamp = kwargs["timestamp"]

        payload = {
            "prediction": prediction,
            "referenced_output": referenced_output,
            "input": input_data,
            "timestamp": timestamp,
            "log_id": log_id,
            "model_id": model_id,
        }
        url = LLM_REGISTER_LOGS(self.project_id)
        headers = self.get_headers()
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            print("Failed to add logs", response.text)
            return
        return response.json()

    def bulk_log(self, *args, **kwargs):
        file_path = kwargs["file"]
        model_id = kwargs["model_id"]
    
        reader = pd.read_csv(file_path, chunksize=BULK_CHUNK_SIZE)
        for i, chunk in enumerate(reader):
            json_data = chunk.to_json(orient="records")
            url = LLM_REGISTER_BULK_LOGS(self.project_id, model_id)
            headers = self.get_headers()
            payload = json.dumps(json_data)
            requests.request("POST", url, headers=headers, data=payload)

        return {
            "status": "success",
            "details": "log insertion completed successfully",
        }
