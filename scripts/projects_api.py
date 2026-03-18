"""
https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api/
"""
import os
import json
import sys
from cvat_sdk import make_client

class ProjectsAPI:
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
    
    # Projects API
    def list_projects(self, filters=None):
        self._connect()
        projects = list(self.client.projects.list(filters=filters))
        result = []
        for project in projects:
            result.append({
                "id": project.id,
                "name": project.name,
                "owner": project.owner,
                "created_date": project.created_date.isoformat() if project.created_date else None,
                "status": project.status
            })
        return result
    
    def get_project(self, project_id):
        self._connect()
        project = self.client.projects.get(project_id)
        return {
            "id": project.id,
            "name": project.name,
            "owner": project.owner,
            "created_date": project.created_date.isoformat() if project.created_date else None,
            "status": project.status,
            "labels": [{
                "name": label.name,
                "color": label.color,
                "attributes": [{
                    "name": attr.name,
                    "mutable": attr.mutable,
                    "values": attr.values
                } for attr in label.attributes]
            } for label in project.labels],
            "tasks": [task.id for task in project.tasks]
        }
    
    def create_project(self, name, labels=None, status=None):
        self._connect()
        project = self.client.projects.create(
            name=name,
            labels=labels or [{"name": "object"}],
            status=status
        )
        return {
            "id": project.id,
            "name": project.name,
            "status": project.status
        }
    
    def update_project(self, project_id, name=None, status=None):
        self._connect()
        project = self.client.projects.get(project_id)
        if name:
            project.name = name
        if status:
            project.status = status
        project.update()
        return {
            "id": project.id,
            "name": project.name,
            "status": project.status
        }
    
    def delete_project(self, project_id):
        self._connect()
        project = self.client.projects.get(project_id)
        project.delete()
        return {"message": f"Project {project_id} deleted successfully"}
    
    def add_labels_to_project(self, project_id, labels):
        self._connect()
        project = self.client.projects.get(project_id)
        for label in labels:
            project.labels.append(label)
        project.update()
        return {
            "id": project.id,
            "labels": [label.name for label in project.labels]
        }
    
    def remove_label_from_project(self, project_id, label_name):
        self._connect()
        project = self.client.projects.get(project_id)
        label_to_remove = None
        for label in project.labels:
            if label.name == label_name:
                label_to_remove = label
                break
        if label_to_remove:
            project.labels.remove(label_to_remove)
            project.update()
        return {
            "id": project.id,
            "labels": [label.name for label in project.labels]
        }
    
    def handle_request(self, request):
        try:
            action = request.get('action')
            
            if not action:
                return {
                    "status": "error",
                    "message": "Action is required"
                }
            
            # Projects actions
            if action == "list_projects":
                filters = request.get('filters')
                result = self.list_projects(filters)
                return {
                    "status": "success",
                    "message": "Projects listed successfully",
                    "data": result
                }
            elif action == "get_project":
                project_id = request.get('project_id')
                if not project_id:
                    return {
                        "status": "error",
                        "message": "Project ID is required"
                    }
                result = self.get_project(project_id)
                return {
                    "status": "success",
                    "message": "Project retrieved successfully",
                    "data": result
                }
            elif action == "create_project":
                name = request.get('name')
                if not name:
                    return {
                        "status": "error",
                        "message": "Project name is required"
                    }
                labels = request.get('labels')
                status = request.get('status')
                result = self.create_project(name, labels, status)
                return {
                    "status": "success",
                    "message": "Project created successfully",
                    "data": result
                }
            elif action == "update_project":
                project_id = request.get('project_id')
                if not project_id:
                    return {
                        "status": "error",
                        "message": "Project ID is required"
                    }
                name = request.get('name')
                status = request.get('status')
                result = self.update_project(project_id, name, status)
                return {
                    "status": "success",
                    "message": "Project updated successfully",
                    "data": result
                }
            elif action == "delete_project":
                project_id = request.get('project_id')
                if not project_id:
                    return {
                        "status": "error",
                        "message": "Project ID is required"
                    }
                result = self.delete_project(project_id)
                return {
                    "status": "success",
                    "message": result["message"]
                }
            elif action == "add_labels_to_project":
                project_id = request.get('project_id')
                labels = request.get('labels')
                if not all([project_id, labels]):
                    return {
                        "status": "error",
                        "message": "Project ID and labels are required"
                    }
                result = self.add_labels_to_project(project_id, labels)
                return {
                    "status": "success",
                    "message": "Labels added to project successfully",
                    "data": result
                }
            elif action == "remove_label_from_project":
                project_id = request.get('project_id')
                label_name = request.get('label_name')
                if not all([project_id, label_name]):
                    return {
                        "status": "error",
                        "message": "Project ID and label name are required"
                    }
                result = self.remove_label_from_project(project_id, label_name)
                return {
                    "status": "success",
                    "message": "Label removed from project successfully",
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
        api = ProjectsAPI()
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