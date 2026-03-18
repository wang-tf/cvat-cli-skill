"""
https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/events-api/
"""
import os
import json
import sys
from cvat_sdk import make_client

class EventsAPI:
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
    
    # Events API
    def list_events(self, filters=None):
        self._connect()
        events = list(self.client.events.list(filters=filters))
        result = []
        for event in events:
            result.append({
                "id": event.id,
                "type": event.type,
                "message": event.message,
                "created_date": event.created_date.isoformat() if event.created_date else None,
                "user": event.user,
                "resource": event.resource,
                "resource_id": event.resource_id
            })
        return result
    
    def get_event(self, event_id):
        self._connect()
        event = self.client.events.get(event_id)
        return {
            "id": event.id,
            "type": event.type,
            "message": event.message,
            "created_date": event.created_date.isoformat() if event.created_date else None,
            "user": event.user,
            "resource": event.resource,
            "resource_id": event.resource_id,
            "details": event.details
        }
    
    def handle_request(self, request):
        try:
            action = request.get('action')
            
            if not action:
                return {
                    "status": "error",
                    "message": "Action is required"
                }
            
            # Events actions
            if action == "list_events":
                filters = request.get('filters')
                result = self.list_events(filters)
                return {
                    "status": "success",
                    "message": "Events listed successfully",
                    "data": result
                }
            elif action == "get_event":
                event_id = request.get('event_id')
                if not event_id:
                    return {
                        "status": "error",
                        "message": "Event ID is required"
                    }
                result = self.get_event(event_id)
                return {
                    "status": "success",
                    "message": "Event retrieved successfully",
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
        api = EventsAPI()
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