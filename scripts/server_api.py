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
        info, _ = self.client.api_client.server_api.retrieve_about()
        return {
            "version": info.version,
            "auth": getattr(info, 'auth', None),
            "analytics": getattr(info, 'analytics', None),
            "documentation": getattr(info, 'documentation', None),
            "feedback": getattr(info, 'feedback', None),
            "support": getattr(info, 'support', None)
        }

    def get_server_health(self):
        self._connect()
        # Since server_health isn't available in this SDK version, let's use retrieve_about as a fallback
        # to at least get the version and return status ok
        info, _ = self.client.api_client.server_api.retrieve_about()
        return {
            "status": "ok",
            "version": info.version
        }
    
    def get_server_config(self):
        self._connect()
        # Since server_config isn't available in this SDK version, let's return what we can
        # from the client config and retrieve_annotation_formats
        annotation_formats, _ = self.client.api_client.server_api.retrieve_annotation_formats()
        return {
            "annotation": annotation_formats.to_dict() if hasattr(annotation_formats, 'to_dict') else {},
            "server": {},
            "oauth": {},
            "cloud_storage": {}
        }
