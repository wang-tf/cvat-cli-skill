import os
import sys

# Set up environment variables for testing
os.environ['CVAT_API_URL'] = 'http://10.205.252.247:8080/'
os.environ['CVAT_USERNAME'] = 'wangtengfei'
os.environ['CVAT_PASSWORD'] = 'wangtf@image123'

from server_api import ServerAPI

def test_server_api():
    """Simple test for Server API"""
    print("Testing Server API...")
    
    # Initialize ServerAPI
    server_api = ServerAPI()
    print("✓ ServerAPI initialized successfully")
    
    # Test get_server_info
    print("Testing get_server_info...")
    try:
        info = server_api.get_server_info()
        print(f"✓ Server info retrieved successfully")
        print(f"  Version: {info.get('version')}")
        print(f"  Auth: {info.get('auth')}")
    except Exception as e:
        print(f"✗ Failed to get server info: {e}")
        return False
    
    # Test get_server_health
    print("Testing get_server_health...")
    try:
        health = server_api.get_server_health()
        print(f"✓ Server health retrieved successfully")
        print(f"  Status: {health.get('status')}")
        print(f"  Version: {health.get('version')}")
    except Exception as e:
        print(f"✗ Failed to get server health: {e}")
        return False
    
    # Test get_server_config
    print("Testing get_server_config...")
    try:
        config = server_api.get_server_config()
        print(f"✓ Server config retrieved successfully")
        print(f"  Annotation config: {config.get('annotation')}")
        print(f"  Server config: {config.get('server')}")
    except Exception as e:
        print(f"✗ Failed to get server config: {e}")
        return False
    
    # Test handle_request
    print("Testing handle_request...")
    try:
        request = {'action': 'get_server_info'}
        response = server_api.handle_request(request)
        if response['status'] == 'success':
            print("✓ handle_request works correctly")
        else:
            print(f"✗ handle_request failed: {response.get('message')}")
            return False
    except Exception as e:
        print(f"✗ Failed to test handle_request: {e}")
        return False
    
    print("\nAll tests passed successfully!")
    return True

if __name__ == '__main__':
    success = test_server_api()
    sys.exit(0 if success else 1)
