"""
https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/labels-api/
"""
import os
import json
import sys
from cvat_sdk import make_client

class LabelsAPI:
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
    
    # Labels API
    def list_labels(self, project_id=None, task_id=None):
        self._connect()
        filters = {}
        if project_id:
            filters['project_id'] = project_id
        if task_id:
            filters['task_id'] = task_id
        
        labels = list(self.client.labels.list(filters=filters))
        result = []
        for label in labels:
            result.append({
                "id": label.id,
                "name": label.name,
                "color": label.color,
                "project_id": label.project_id,
                "task_id": label.task_id
            })
        return result
    
    def get_label(self, label_id):
        self._connect()
        label = self.client.labels.get(label_id)
        return {
            "id": label.id,
            "name": label.name,
            "color": label.color,
            "project_id": label.project_id,
            "task_id": label.task_id,
            "attributes": [{
                "name": attr.name,
                "mutable": attr.mutable,
                "values": attr.values
            } for attr in label.attributes]
        }
    
    def create_label(self, name, color=None, project_id=None, task_id=None, attributes=None):
        self._connect()
        label = self.client.labels.create(
            name=name,
            color=color,
            project_id=project_id,
            task_id=task_id,
            attributes=attributes
        )
        return {
            "id": label.id,
            "name": label.name,
            "color": label.color,
            "project_id": label.project_id,
            "task_id": label.task_id
        }
    
    def update_label(self, label_id, name=None, color=None):
        self._connect()
        label = self.client.labels.get(label_id)
        if name:
            label.name = name
        if color:
            label.color = color
        label.update()
        return {
            "id": label.id,
            "name": label.name,
            "color": label.color
        }
    
    def delete_label(self, label_id):
        self._connect()
        label = self.client.labels.get(label_id)
        label.delete()
        return {"message": f"Label {label_id} deleted successfully"}
    
    def handle_request(self, request):
        try:
            action = request.get('action')
            
            if not action:
                return {
                    "status": "error",
                    "message": "Action is required"
                }
            
            # Labels actions
            if action == "list_labels":
                project_id = request.get('project_id')
                task_id = request.get('task_id')
                result = self.list_labels(project_id, task_id)
                return {
                    "status": "success",
                    "message": "Labels listed successfully",
                    "data": result
                }
            elif action == "get_label":
                label_id = request.get('label_id')
                if not label_id:
                    return {
                        "status": "error",
                        "message": "Label ID is required"
                    }
                result = self.get_label(label_id)
                return {
                    "status": "success",
                    "message": "Label retrieved successfully",
                    "data": result
                }
            elif action == "create_label":
                name = request.get('name')
                if not name:
                    return {
                        "status": "error",
                        "message": "Label name is required"
                    }
                color = request.get('color')
                project_id = request.get('project_id')
                task_id = request.get('task_id')
                attributes = request.get('attributes')
                result = self.create_label(name, color, project_id, task_id, attributes)
                return {
                    "status": "success",
                    "message": "Label created successfully",
                    "data": result
                }
            elif action == "update_label":
                label_id = request.get('label_id')
                if not label_id:
                    return {
                        "status": "error",
                        "message": "Label ID is required"
                    }
                name = request.get('name')
                color = request.get('color')
                result = self.update_label(label_id, name, color)
                return {
                    "status": "success",
                    "message": "Label updated successfully",
                    "data": result
                }
            elif action == "delete_label":
                label_id = request.get('label_id')
                if not label_id:
                    return {
                        "status": "error",
                        "message": "Label ID is required"
                    }
                result = self.delete_label(label_id)
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
        api = LabelsAPI()
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