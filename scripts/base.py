import os
import json
from cvat_sdk import make_client


class CVATBase:
    def __init__(self):
        self.cvat_host = os.environ.get('CVAT_HOST')
        self.cvat_username = os.environ.get('CVAT_USERNAME')
        self.cvat_password = os.environ.get('CVAT_PASSWORD')
        self._check_config()
        self.client = None

    def _check_config(self):
        if not all([self.cvat_host, self.cvat_username, self.cvat_password]):
            raise ValueError("Missing required environment variables: CVAT_HOST, CVAT_USERNAME, CVAT_PASSWORD")

    def _connect(self):
        if not self.client:
            self.client = make_client(
                self.cvat_host,
                credentials=(self.cvat_username, self.cvat_password)
            )

    def success_response(self, message, data=None):
        return {
            "status": "success",
            "message": message,
            "data": data
        }

    def error_response(self, message):
        return {
            "status": "error",
            "message": message
        }


def print_response(response):
    print(json.dumps(response, indent=2, ensure_ascii=False))
