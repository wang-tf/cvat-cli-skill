"""
https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/assets-api/
"""
import os
import json
import sys
from cvat_sdk import make_client

class AssetsAPI:
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
    
    # Assets API
    def list_assets(self, filters=None):
        self._connect()
        assets = list(self.client.assets.list(filters=filters))
        result = []
        for asset in assets:
            result.append({
                "id": asset.id,
                "name": asset.name,
                "size": asset.size,
                "content_type": asset.content_type,
                "owner": asset.owner,
                "created_date": asset.created_date.isoformat() if asset.created_date else None,
                "updated_date": asset.updated_date.isoformat() if asset.updated_date else None
            })
        return result
    
    def get_asset(self, asset_id):
        self._connect()
        asset = self.client.assets.get(asset_id)
        return {
            "id": asset.id,
            "name": asset.name,
            "size": asset.size,
            "content_type": asset.content_type,
            "owner": asset.owner,
            "created_date": asset.created_date.isoformat() if asset.created_date else None,
            "updated_date": asset.updated_date.isoformat() if asset.updated_date else None
        }
    
    def create_asset(self, name, file_path):
        self._connect()
        with open(file_path, 'rb') as f:
            asset = self.client.assets.create(
                name=name,
                file=f
            )
        return {
            "id": asset.id,
            "name": asset.name,
            "size": asset.size,
            "content_type": asset.content_type
        }
    
    def delete_asset(self, asset_id):
        self._connect()
        asset = self.client.assets.get(asset_id)
        asset.delete()
        return {"message": f"Asset {asset_id} deleted successfully"}
    
    def handle_request(self, request):
        try:
            action = request.get('action')
            
            if not action:
                return {
                    "status": "error",
                    "message": "Action is required"
                }
            
            # Assets actions
            if action == "list_assets":
                filters = request.get('filters')
                result = self.list_assets(filters)
                return {
                    "status": "success",
                    "message": "Assets listed successfully",
                    "data": result
                }
            elif action == "get_asset":
                asset_id = request.get('asset_id')
                if not asset_id:
                    return {
                        "status": "error",
                        "message": "Asset ID is required"
                    }
                result = self.get_asset(asset_id)
                return {
                    "status": "success",
                    "message": "Asset retrieved successfully",
                    "data": result
                }
            elif action == "create_asset":
                name = request.get('name')
                file_path = request.get('file_path')
                if not all([name, file_path]):
                    return {
                        "status": "error",
                        "message": "Name and file path are required"
                    }
                result = self.create_asset(name, file_path)
                return {
                    "status": "success",
                    "message": "Asset created successfully",
                    "data": result
                }
            elif action == "delete_asset":
                asset_id = request.get('asset_id')
                if not asset_id:
                    return {
                        "status": "error",
                        "message": "Asset ID is required"
                    }
                result = self.delete_asset(asset_id)
                return {
                    "status": "success",
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
        api = AssetsAPI()
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