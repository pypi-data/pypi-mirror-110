import requests

from requests.auth import HTTPBasicAuth
from importlib import import_module

from slai.config import get_api_base_url
from slai.modules.parameters import from_config
from slai.modules.runtime import detect_runtime, detect_credentials

REQUESTS_TIMEOUT = 15


def get_cli_client(client_id=None, client_secret=None):
    import_path = from_config(
        "CLI_CLIENT",
        "slai.clients.cli.SlaiCliClient",
    )
    class_ = import_path.split(".")[-1]
    path = ".".join(import_path.split(".")[:-1])
    return getattr(import_module(path), class_)(
        client_id=client_id, client_secret=client_secret
    )


class SlaiCliClient:
    BASE_URL = get_api_base_url()

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        user_agent_header="SlaiCli smartshare/0.1.0",
    ):
        self.runtime = detect_runtime()

        if client_id is None or client_secret is None:
            credentials = detect_credentials(runtime=self.runtime)
            self.client_id = credentials["client_id"]
            self.client_secret = credentials["client_secret"]
        else:
            self.client_id = client_id
            self.client_secret = client_secret

        self.user_agent_header = user_agent_header

    def create_project(self, name):
        body = {"action": "create", "name": name}

        res = requests.post(
            f"{self.BASE_URL}/cli/project",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def retrieve_project(self, *, project_name):
        body = {"action": "retrieve", "name": project_name}

        res = requests.post(
            f"{self.BASE_URL}/cli/project",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def update_project(self, project_name):
        body = {
            "action": "update",
            "name": project_name,
        }

        res = requests.post(
            f"{self.BASE_URL}/cli/project",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def create_model(self, *, project_name, name):
        body = {"action": "create", "name": name, "project_name": project_name}

        res = requests.post(
            f"{self.BASE_URL}/cli/model",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def retrieve_model(self, *, project_name, name):
        body = {
            "action": "retrieve",
            "name": name,
            "project_name": project_name,
        }

        body = {k: v for k, v in body.items() if v is not None}

        res = requests.post(
            f"{self.BASE_URL}/cli/model",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def create_model_version(self, *, model_id, name):
        body = {"action": "create", "model_id": model_id, "name": name}

        res = requests.post(
            f"{self.BASE_URL}/cli/model-version",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def retrieve_model_version_by_name(self, *, model_id, model_version_name):
        body = {
            "action": "retrieve",
            "model_id": model_id,
            "model_version_name": model_version_name,
        }

        res = requests.post(
            f"{self.BASE_URL}/cli/model-version",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def retrieve_model_version_by_id(self, *, model_version_id):
        body = {
            "action": "retrieve",
            "model_version_id": model_version_id,
        }

        res = requests.post(
            f"{self.BASE_URL}/cli/model-version",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def list_model_versions(self, *, model_id):
        body = {"action": "list", "model_id": model_id}

        res = requests.post(
            f"{self.BASE_URL}/cli/model-version",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def retrieve_model_artifact(self, *, model_version_id, model_artifact_id):
        body = {
            "action": "retrieve",
            "model_version_id": model_version_id,
            "model_artifact_id": model_artifact_id,
        }

        body = {k: v for k, v in body.items() if v is not None}

        res = requests.post(
            f"{self.BASE_URL}/cli/model-artifact",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def create_model_artifact(
        self,
        *,
        model_version_id,
        model_data,
        artifact_type,
        artifact_notebook,
        artifact_requirements,
        custom_metadata,
    ):
        body = {
            "action": "create",
            "model_version_id": model_version_id,
            "model_data": model_data,
            "artifact_type": artifact_type,
            "artifact_notebook": artifact_notebook,
            "artifact_requirements": artifact_requirements,
            "custom_metadata": custom_metadata,
        }

        res = requests.post(
            f"{self.BASE_URL}/cli/model-artifact",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def create_model_deployment(
        self,
        *,
        model_artifact_id,
        model_handler_data,
        requirements,
    ):
        body = {
            "action": "create",
            "model_artifact_id": model_artifact_id,
            "model_handler_data": model_handler_data,
            "requirements": requirements,
        }

        res = requests.post(
            f"{self.BASE_URL}/cli/deploy",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def update_model(self, *, model_data):
        body = model_data
        body["action"] = "update"

        # TODO: refactor this, this is weird
        model_id = body["id"]
        body["model_id"] = model_id

        del body["created"]
        del body["updated"]

        body = {k: v for k, v in body.items() if v is not None}
        res = requests.post(
            f"{self.BASE_URL}/cli/model",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def get_user(self):
        body = {"action": "retrieve"}

        res = requests.post(
            f"{self.BASE_URL}/cli/user",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def update_user(self, email=None, gauth_creds=None):
        body = {"action": "update", "email": email, "gauth_creds": gauth_creds}

        body = {k: v for k, v in body.items() if v is not None}
        res = requests.post(
            f"{self.BASE_URL}/cli/user",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def get_cli_version(self):
        body = {}
        res = requests.post(
            f"{self.BASE_URL}/cli/cli-version",
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()


class MockSlaiCliClient:
    BASE_URL = from_config(
        key="BASE_URL",
        default="https://6zacu5yc29.execute-api.us-east-1.amazonaws.com/development",
    )

    def __init__(
        self, *, client_id, client_secret, user_agent_header="SlaiCli smartshare/0.1.0"
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent_header = user_agent_header

    def create_project(self, name):
        return {
            "id": "603299d4dd191a68cfb474ee",
            "name": name,
            "created": "2021-02-21T12:35:16.248099",
            "updated": "2021-02-21T12:35:16.293876",
        }

    def retrieve_project(self, *, name):
        return {
            "id": "some_project_id",
            "name": "some_project",
            "created": "2021-02-21T12:35:16.248099",
            "updated": "2021-02-21T12:35:16.293876",
        }

    def update_project(self, name):
        return {
            "id": "some_project_id",
            "name": name,
            "created": "2021-02-21T12:35:16.248099",
            "updated": "2021-02-21T12:35:16.293876",
        }

    def create_model(self, *, project_name, name):
        return {
            "id": "60329220dd191a68cfb474ec",
            "name": name,
            "model_s3_data_bucket_name": None,
            "notebook_uri": None,
            "model_version_id": "60329220dd191a68cfb474ed",
            "created": "2021-02-21T12:02:24.503850",
            "updated": "2021-02-21T12:02:24.635203",
        }

    def retrieve_model(self, *, project_name, name):
        return {
            "id": "some_model_id",
            "name": name,
            "model_s3_data_bucket_name": None,
            "notebook_uri": None,
            "model_version_id": "60329220dd191a68cfb474ed",
            "created": "2021-02-21T12:02:24.503850",
            "updated": "2021-02-21T12:02:24.635203",
        }

    def update_model(self, *, model_data):
        return model_data

    def create_model_artifact(self, *, model_version_id, model_data, artifact_type):
        return {
            "id": "some_model_artifact_id",
            "model_version_id": model_version_id,
            "artifact_type": artifact_type,
            "created": "2021-02-28T12:04:26.737777",
        }

    def retrieve_model_artifact(self, *, model_version_id, model_artifact_id):
        return {
            "id": model_artifact_id,
            "model_version_id": model_version_id,
            "artifact_type": "TORCH",
            "created": "2021-02-28T12:04:26.737777",
        }

    def create_model_deployment(
        self,
        *,
        model_artifact_id,
        model_handler_data,
        model_handler_requirements,
    ):
        return {
            "id": "some_model_id",
            "created": "2021-02-21T12:02:24.503850",
            "updated": "2021-02-21T12:02:24.635203",
        }
