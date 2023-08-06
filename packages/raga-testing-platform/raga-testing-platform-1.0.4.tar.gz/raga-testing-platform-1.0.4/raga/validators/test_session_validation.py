
class TestSessionValidator:

    @staticmethod
    def validate_token(token: str) -> str:
        if not token:
            raise ValueError("Token is required.")
        # Additional validation logic specific to token
        return token

    @staticmethod
    def validate_project_id(project_id: int) -> int:
        if not project_id:
            raise ValueError("Project id is required.")
        # Additional validation logic specific to project id
        return project_id

    @staticmethod
    def validate_run_name(run_name: str) -> str:
        if not run_name:
            raise ValueError("Run name is required.")
        # Additional validation logic specific to run name
        return run_name


