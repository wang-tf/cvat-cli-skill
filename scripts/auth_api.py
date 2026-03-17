import os
import json
import sys
from cvat_sdk import make_client

class AuthAPI:
    def __init__(self):
        self.cvat_api_url = os.environ.get('CVAT_API_URL')
        self.cvat_username = os.environ.get('CVAT_USERNAME')
        self.cvat_password = os.environ.get('CVAT_PASSWORD')
        self._check_config()
        self.client = None
    
    def _check_config(self):
        if not self.cvat_api_url:
            raise ValueError("Missing required environment variable: CVAT_API_URL")
    
    def _connect(self, username=None, password=None):
        if not self.client:
            self.client = make_client(
                self.cvat_api_url,
                credentials=(username or self.cvat_username, password or self.cvat_password)
            )
    
    # Auth API
    def login(self, username, password):
        # Create a new client with the provided credentials
        client = make_client(
            self.cvat_api_url,
            credentials=(username, password)
        )
        # Check if login was successful by accessing user info
        user = client.users.get_current()
        return {
            "status": "success",
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    
    def logout(self):
        self._connect()
        # In CVAT SDK, logout is handled by closing the session
        # This is automatically done when the client is garbage collected
        # For completeness, we'll just return a success message
        return {
            "status": "success",
            "message": "Logout successful"
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
            
            # Auth actions
            if action == "login":
                username = request.get('username')
                password = request.get('password')
                if not all([username, password]):
                    return {
                        "status": "error",
                        "message": "Username and password are required"
                    }
                result = self.login(username, password)
                return result
            elif action == "logout":
                result = self.logout()
                return result
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
        api = AuthAPI()
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