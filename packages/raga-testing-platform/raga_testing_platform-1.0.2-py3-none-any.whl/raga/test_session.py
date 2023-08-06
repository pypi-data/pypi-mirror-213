import json
from raga.validators.test_session_validation import TestSessionValidator
from raga.utils.http_client import HTTPClient
from raga.utils.raga_config_reader import read_raga_config, get_config_value

config_data = read_raga_config(".raga")

class TestSession:
    def __init__(self, token: str, project_id: str, run_name: str):
        self.token = TestSessionValidator.validate_token(token)
        self.project_id = TestSessionValidator.validate_project_id(project_id)
        self.run_name = TestSessionValidator.validate_run_name(run_name)
        self.http_client = HTTPClient(get_config_value(config_data, 'default', 'api_host'))
        self.experiment_id = self.create_experiment()
    
    def create_experiment(self):
        """
        Creates an experiment by sending a request to the Raga API.

        Returns:
            str: The ID of the created experiment.

        Raises:
            KeyError: If the response data does not contain a valid experiment ID.
        """
        res_data = self.http_client.post(
            "api/experiments",
            {"name": self.run_name, "projectId": self.project_id},
            {"Authorization": f'Bearer {self.token}'},
        )
        experiment_id = res_data.get("data", {}).get("id")
        if not experiment_id:
            raise KeyError("Invalid response data. Experiment ID not found.")
        return experiment_id
