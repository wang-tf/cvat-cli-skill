import os
import json
import sys
from cvat_sdk import make_client

class CVATCLITools:
    def __init__(self):
        self.cvat_host = os.environ.get('CVAT_HOST') or os.environ.get('CVAT_API_URL')
        self.cvat_username = os.environ.get('CVAT_USERNAME')
        self.cvat_password = os.environ.get('CVAT_PASSWORD')
        self._check_config()
        self.client = None

    def _check_config(self):
        if not all([self.cvat_host, self.cvat_username, self.cvat_password]):
            raise ValueError("Missing required environment variables: CVAT_HOST (or CVAT_API_URL), CVAT_USERNAME, CVAT_PASSWORD")

    def _connect(self):
        if not self.client:
            self.client = make_client(
                self.cvat_host,
                credentials=(self.cvat_username, self.cvat_password)
            )

    # Implementations API
    def list_implementations(self):
        self._connect()
        implementations = list(self.client.implementations.list())
        result = []
        for impl in implementations:
            result.append({
                "id": impl.id,
                "name": impl.name,
                "framework": impl.framework,
                "description": impl.description
            })
        return result
