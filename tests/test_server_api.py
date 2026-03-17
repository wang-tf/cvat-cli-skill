import os
import sys
import json
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.server_api import ServerAPI


class TestServerAPI:
    def setup_method(self):
        """Set up test fixtures"""
        self.server_api = ServerAPI()
    
    def test_initialization(self):
        """Test that ServerAPI initializes correctly"""
        assert self.server_api.cvat_api_url is not None
        assert self.server_api.cvat_username is not None
        assert self.server_api.cvat_password is not None
        assert self.server_api.client is None

    def test_get_server_info(self):
        """Test get_server_info method"""
        info = self.server_api.get_server_info()
        assert isinstance(info, dict)
        assert 'version' in info
        assert 'auth' in info
        assert 'analytics' in info
        assert 'documentation' in info
        assert 'feedback' in info
        assert 'support' in info
    
    def test_get_server_health(self):
        """Test get_server_health method"""
        health = self.server_api.get_server_health()
        assert isinstance(health, dict)
        assert 'status' in health
        assert 'version' in health
        assert health['status'] == 'ok'  # Assuming server is healthy
    
    def test_get_server_config(self):
        """Test get_server_config method"""
        config = self.server_api.get_server_config()
        assert isinstance(config, dict)
        assert 'annotation' in config
        assert 'server' in config
        assert 'oauth' in config
        assert 'cloud_storage' in config


if __name__ == '__main__':
    pytest.main(['-v', __file__])
