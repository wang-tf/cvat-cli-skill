"""
https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/users-api/
"""
import os
import json
import sys
from cvat_sdk import make_client

class UsersAPI:
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
    
    # Users API
    def list_users(self, filters=None):
        self._connect()
        users = list(self.client.users.list(filters=filters))
        result = []
        for user in users:
            result.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "date_joined": user.date_joined.isoformat() if user.date_joined else None,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser
            })
        return result
    
    def get_user(self, user_id):
        self._connect()
        user = self.client.users.get(user_id)
        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "date_joined": user.date_joined.isoformat() if user.date_joined else None,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser
        }
    
    def get_current_user(self):
        self._connect()
        user = self.client.users.get_current()
        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "date_joined": user.date_joined.isoformat() if user.date_joined else None,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser
        }
    
    def handle_request(self, request):
        try:
            action = request.get('action')
            
            if not action:
                return {
                    "status": "error",
                    "message": "Action is required"
                }
            
            # Users actions
            if action == "list_users":
                filters = request.get('filters')
                result = self.list_users(filters)
                return {
                    "status": "success",
                    "message": "Users listed successfully",
                    "data": result
                }
            elif action == "get_user":
                user_id = request.get('user_id')
                if not user_id:
                    return {
                        "status": "error",
                        "message": "User ID is required"
                    }
                result = self.get_user(user_id)
                return {
                    "status": "success",
                    "message": "User retrieved successfully",
                    "data": result
                }
            elif action == "get_current_user":
                result = self.get_current_user()
                return {
                    "status": "success",
                    "message": "Current user retrieved successfully",
                    "data": result
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
        api = UsersAPI()
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