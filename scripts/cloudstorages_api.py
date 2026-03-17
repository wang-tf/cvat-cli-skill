import os
import json
import sys
from cvat_sdk import make_client

class CloudStoragesAPI:
    def __init__(self):
        self.cvat_api_url = os.environ.get('CVAT_API_URL')
        self.cvat_username = os.environ.get('CVAT_USERNAME')
        self.cvat_password = os.environ.get('CVAT_PASSWORD')
        self._check_config()
        self.client = None
    
    def _check_config(self):
        if not all([self.cvat_api_url, self.cvat_username, self.cvat_password]):
            raise ValueError("Missing required environment variables: CVAT_API_URL, CVAT_USERNAME, CVAT_PASSWORD")
    
    def _connect(self):
        if not self.client:
            self.client = make_client(
                self.cvat_api_url,
                credentials=(self.cvat_username, self.cvat_password)
            )
    
    # Cloud Storages API
    def list_cloud_storages(self, filters=None):
        self._connect()
        storages = list(self.client.cloud_storages.list(filters=filters))
        result = []
        for storage in storages:
            result.append({
                "id": storage.id,
                "name": storage.name,
                "type": storage.type,
                "owner": storage.owner,
                "created_date": storage.created_date.isoformat() if storage.created_date else None,
                "status": storage.status
            })
        return result
    
    def get_cloud_storage(self, storage_id):
        self._connect()
        storage = self.client.cloud_storages.get(storage_id)
        return {
            "id": storage.id,
            "name": storage.name,
            "type": storage.type,
            "owner": storage.owner,
            "created_date": storage.created_date.isoformat() if storage.created_date else None,
            "status": storage.status,
            "configuration": storage.configuration,
            "endpoint": storage.endpoint
        }
    
    def create_cloud_storage(self, name, type, configuration, endpoint=None):
        self._connect()
        storage = self.client.cloud_storages.create(
            name=name,
            type=type,
            configuration=configuration,
            endpoint=endpoint
        )
        return {
            "id": storage.id,
            "name": storage.name,
            "type": storage.type,
            "status": storage.status
        }
    
    def update_cloud_storage(self, storage_id, name=None, configuration=None, endpoint=None):
        self._connect()
        storage = self.client.cloud_storages.get(storage_id)
        if name:
            storage.name = name
        if configuration:
            storage.configuration = configuration
        if endpoint:
            storage.endpoint = endpoint
        storage.update()
        return {
            "id": storage.id,
            "name": storage.name,
            "type": storage.type,
            "status": storage.status
        }
    
    def delete_cloud_storage(self, storage_id):
        self._connect()
        storage = self.client.cloud_storages.get(storage_id)
        storage.delete()
        return {"message": f"Cloud storage {storage_id} deleted successfully"}
    
    def test_cloud_storage(self, storage_id):
        self._connect()
        storage = self.client.cloud_storages.get(storage_id)
        result = storage.test()
        return {
            "status": "success" if result else "error",
            "message": "Cloud storage test passed" if result else "Cloud storage test failed"
        }
    
    def handle_request(self, request):
        try:
            action = request.get('action')
            
            if not action:
                return {
                    "status": "error",
                    "message": "Action is required"
                }
            
            # Cloud Storages actions
            if action == "list_cloud_storages":
                filters = request.get('filters')
                result = self.list_cloud_storages(filters)
                return {
                    "status": "success",
                    "message": "Cloud storages listed successfully",
                    "data": result
                }
            elif action == "get_cloud_storage":
                storage_id = request.get('storage_id')
                if not storage_id:
                    return {
                        "status": "error",
                        "message": "Storage ID is required"
                    }
                result = self.get_cloud_storage(storage_id)
                return {
                    "status": "success",
                    "message": "Cloud storage retrieved successfully",
                    "data": result
                }
            elif action == "create_cloud_storage":
                name = request.get('name')
                type = request.get('type')
                configuration = request.get('configuration')
                
                if not all([name, type, configuration]):
                    return {
                        "status": "error",
                        "message": "Name, type, and configuration are required"
                    }
                
                endpoint = request.get('endpoint')
                result = self.create_cloud_storage(name, type, configuration, endpoint)
                return {
                    "status": "success",
                    "message": "Cloud storage created successfully",
                    "data": result
                }
            elif action == "update_cloud_storage":
                storage_id = request.get('storage_id')
                if not storage_id:
                    return {
                        "status": "error",
                        "message": "Storage ID is required"
                    }
                
                name = request.get('name')
                configuration = request.get('configuration')
                endpoint = request.get('endpoint')
                result = self.update_cloud_storage(storage_id, name, configuration, endpoint)
                return {
                    "status": "success",
                    "message": "Cloud storage updated successfully",
                    "data": result
                }
            elif action == "delete_cloud_storage":
                storage_id = request.get('storage_id')
                if not storage_id:
                    return {
                        "status": "error",
                        "message": "Storage ID is required"
                    }
                
                result = self.delete_cloud_storage(storage_id)
                return {
                    "status": "success",
                    "message": result["message"]
                }
            elif action == "test_cloud_storage":
                storage_id = request.get('storage_id')
                if not storage_id:
                    return {
                        "status": "error",
                        "message": "Storage ID is required"
                    }
                
                result = self.test_cloud_storage(storage_id)
                return {
                    "status": result["status"],
                    "message": result["message"]
                }
            else:
                return {
                    "status": "error",
                    "message": f"Action not supported: {action}"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

def main():
    if len(sys.argv) != 2:
        print(json.dumps({
            "status": "error",
            "message": "Expected exactly one argument: the JSON request"
        }))
        sys.exit(1)
    
    try:
        request = json.loads(sys.argv[1])
        api = CloudStoragesAPI()
        response = api.handle_request(request)
        print(json.dumps(response))
    except json.JSONDecodeError:
        print(json.dumps({
            "status": "error",
            "message": "Invalid JSON request"
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()