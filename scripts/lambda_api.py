"""
https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/lambda-api/
"""
import os
import json
import sys
from cvat_sdk import make_client

class LambdaAPI:
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
    
    # Lambda API
    def list_lambdas(self, filters=None):
        self._connect()
        lambdas = list(self.client.lambdas.list(filters=filters))
        result = []
        for lambda_func in lambdas:
            result.append({
                "id": lambda_func.id,
                "name": lambda_func.name,
                "owner": lambda_func.owner,
                "created_date": lambda_func.created_date.isoformat() if lambda_func.created_date else None,
                "status": lambda_func.status,
                "runtime": lambda_func.runtime
            })
        return result
    
    def get_lambda(self, lambda_id):
        self._connect()
        lambda_func = self.client.lambdas.get(lambda_id)
        return {
            "id": lambda_func.id,
            "name": lambda_func.name,
            "owner": lambda_func.owner,
            "created_date": lambda_func.created_date.isoformat() if lambda_func.created_date else None,
            "status": lambda_func.status,
            "runtime": lambda_func.runtime,
            "description": lambda_func.description,
            "entrypoint": lambda_func.entrypoint,
            "memory_limit": lambda_func.memory_limit,
            "timeout": lambda_func.timeout
        }
    
    def create_lambda(self, name, runtime, entrypoint, description=None, memory_limit=128, timeout=30):
        self._connect()
        lambda_func = self.client.lambdas.create(
            name=name,
            runtime=runtime,
            entrypoint=entrypoint,
            description=description,
            memory_limit=memory_limit,
            timeout=timeout
        )
        return {
            "id": lambda_func.id,
            "name": lambda_func.name,
            "status": lambda_func.status
        }
    
    def update_lambda(self, lambda_id, name=None, description=None, memory_limit=None, timeout=None):
        self._connect()
        lambda_func = self.client.lambdas.get(lambda_id)
        if name:
            lambda_func.name = name
        if description:
            lambda_func.description = description
        if memory_limit:
            lambda_func.memory_limit = memory_limit
        if timeout:
            lambda_func.timeout = timeout
        lambda_func.update()
        return {
            "id": lambda_func.id,
            "name": lambda_func.name,
            "status": lambda_func.status
        }
    
    def delete_lambda(self, lambda_id):
        self._connect()
        lambda_func = self.client.lambdas.get(lambda_id)
        lambda_func.delete()
        return {"message": f"Lambda function {lambda_id} deleted successfully"}
    
    def upload_lambda_code(self, lambda_id, code_path):
        self._connect()
        lambda_func = self.client.lambdas.get(lambda_id)
        with open(code_path, 'rb') as f:
            lambda_func.upload_code(f)
        return {"message": f"Code uploaded successfully for lambda function {lambda_id}"}
    
    def handle_request(self, request):
        try:
            action = request.get('action')
            
            if not action:
                return {
                    "status": "error",
                    "message": "Action is required"
                }
            
            # Lambda actions
            if action == "list_lambdas":
                filters = request.get('filters')
                result = self.list_lambdas(filters)
                return {
                    "status": "success",
                    "message": "Lambda functions listed successfully",
                    "data": result
                }
            elif action == "get_lambda":
                lambda_id = request.get('lambda_id')
                if not lambda_id:
                    return {
                        "status": "error",
                        "message": "Lambda ID is required"
                    }
                result = self.get_lambda(lambda_id)
                return {
                    "status": "success",
                    "message": "Lambda function retrieved successfully",
                    "data": result
                }
            elif action == "create_lambda":
                name = request.get('name')
                runtime = request.get('runtime')
                entrypoint = request.get('entrypoint')
                
                if not all([name, runtime, entrypoint]):
                    return {
                        "status": "error",
                        "message": "Name, runtime, and entrypoint are required"
                    }
                
                description = request.get('description')
                memory_limit = request.get('memory_limit', 128)
                timeout = request.get('timeout', 30)
                
                result = self.create_lambda(name, runtime, entrypoint, description, memory_limit, timeout)
                return {
                    "status": "success",
                    "message": "Lambda function created successfully",
                    "data": result
                }
            elif action == "update_lambda":
                lambda_id = request.get('lambda_id')
                if not lambda_id:
                    return {
                        "status": "error",
                        "message": "Lambda ID is required"
                    }
                
                name = request.get('name')
                description = request.get('description')
                memory_limit = request.get('memory_limit')
                timeout = request.get('timeout')
                
                result = self.update_lambda(lambda_id, name, description, memory_limit, timeout)
                return {
                    "status": "success",
                    "message": "Lambda function updated successfully",
                    "data": result
                }
            elif action == "delete_lambda":
                lambda_id = request.get('lambda_id')
                if not lambda_id:
                    return {
                        "status": "error",
                        "message": "Lambda ID is required"
                    }
                
                result = self.delete_lambda(lambda_id)
                return {
                    "status": "success",
                    "message": result["message"]
                }
            elif action == "upload_lambda_code":
                lambda_id = request.get('lambda_id')
                code_path = request.get('code_path')
                
                if not all([lambda_id, code_path]):
                    return {
                        "status": "error",
                        "message": "Lambda ID and code path are required"
                    }
                
                result = self.upload_lambda_code(lambda_id, code_path)
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
        api = LambdaAPI()
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