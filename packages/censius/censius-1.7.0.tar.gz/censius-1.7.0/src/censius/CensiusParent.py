class CensiusParent(object):
    def __init__(self, api_key, project_id):
        if api_key == None or len(api_key) == 0:
            raise ValueError("API Key can't be empty and should be a string")
        if project_id == None or type(project_id) != int:
            raise ValueError("Project Id can't be empty and should be an integer")
        self.api_key = api_key
        self.project_id = project_id

    def update_project_id(self, project_id):
        self.project_id = project_id

    def update_api_key(self, api_key):
        self.api_key = api_key

    def get_headers(self):
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json",
        }
