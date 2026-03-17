"""
https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/server-api/
"""
import os
import json
import sys
from cvat_sdk import make_client

class ServerAPI:
    def __init__(self):
        self.cvat_api_url = os.environ.get('CVAT_API_URL')
        self.cvat_username = os.environ.get('CVAT_USERNAME')
        self.cvat_password = os.environ.get('CVAT_PASSWORD')
        self._check_config()
        self.client = None
    
    def _check_config(self):
        if not self.cvat_api_url:
            raise ValueError("Missing required environment variable: CVAT_API_URL")
    
    def _connect(self):
        if not self.client:
            # For server API, we can use an unauthenticated client if needed
            if self.cvat_username and self.cvat_password:
                self.client = make_client(
                    self.cvat_api_url,
                    credentials=(self.cvat_username, self.cvat_password)
                )
            else:
                self.client = make_client(self.cvat_api_url)
    
    # Server API
    def get_server_info(self):
        self._connect()
        info = self.client.server.get_info()
        return {
            "version": info.version,
            "auth": info.auth,
            "analytics": info.analytics,
            "documentation": info.documentation,
            "feedback": info.feedback,
            "support": info.support
        }
    
    def get_server_health(self):
        self._connect()
        health = self.client.server.get_health()
        return {
            "status": health.status,
            "version": health.version
        }
    
    def get_server_config(self):
        self._connect()
        config = self.client.server.get_config()
        return {
            "annotation": config.annotation,
            "server": config.server,
            "oauth": config.oauth,
            "cloud_storage": config.cloud_storage
        }
