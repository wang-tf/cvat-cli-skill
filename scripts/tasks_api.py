"""
https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api/
"""
import os
import json
import sys
from cvat_sdk import make_client

class TasksAPI:
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
    
    # Tasks API
    def list_tasks(self, filters=None):
        self._connect()
        tasks = list(self.client.tasks.list(filters=filters))
        result = []
        for task in tasks:
            result.append({
                "id": task.id,
                "name": task.name,
                "status": task.status,
                "project_id": task.project_id,
                "owner": task.owner,
                "created_date": task.created_date.isoformat() if task.created_date else None,
                "updated_date": task.updated_date.isoformat() if task.updated_date else None
            })
        return result
    
    def get_task(self, task_id):
        self._connect()
        task = self.client.tasks.get(task_id)
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status,
            "project_id": task.project_id,
            "owner": task.owner,
            "created_date": task.created_date.isoformat() if task.created_date else None,
            "updated_date": task.updated_date.isoformat() if task.updated_date else None,
            "labels": [{
                "name": label.name,
                "color": label.color,
                "attributes": [{
                    "name": attr.name,
                    "mutable": attr.mutable,
                    "values": attr.values
                } for attr in label.attributes]
            } for label in task.labels],
            "data": task.data,
            "segments": [{
                "id": segment.id,
                "start_frame": segment.start_frame,
                "stop_frame": segment.stop_frame
            } for segment in task.segments],
            "jobs": [job.id for job in task.jobs]
        }
    
    def create_task(self, name, labels=None, project_id=None, data=None, status=None):
        self._connect()
        task = self.client.tasks.create(
            name=name,
            labels=labels or [{"name": "object"}],
            project_id=project_id,
            data=data or [],
            status=status
        )
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status
        }
    
    def update_task(self, task_id, name=None, status=None):
        self._connect()
        task = self.client.tasks.get(task_id)
        if name:
            task.name = name
        if status:
            task.status = status
        task.update()
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status
        }
    
    def delete_task(self, task_id):
        self._connect()
        task = self.client.tasks.get(task_id)
        task.delete()
        return {"message": f"Task {task_id} deleted successfully"}
    
    def add_labels_to_task(self, task_id, labels):
        self._connect()
        task = self.client.tasks.get(task_id)
        for label in labels:
            task.labels.append(label)
        task.update()
        return {
            "id": task.id,
            "labels": [label.name for label in task.labels]
        }
    
    def remove_label_from_task(self, task_id, label_name):
        self._connect()
        task = self.client.tasks.get(task_id)
        label_to_remove = None
        for label in task.labels:
            if label.name == label_name:
                label_to_remove = label
                break
        if label_to_remove:
            task.labels.remove(label_to_remove)
            task.update()
        return {
            "id": task.id,
            "labels": [label.name for label in task.labels]
        }
    
    def handle_request(self, request):
        try:
            action = request.get('action')
            
            if not action:
                return {
                    "status": "error",
                    "message": "Action is required"
                }
            
            # Tasks actions
            if action == "list_tasks":
                filters = request.get('filters')
                result = self.list_tasks(filters)
                return {
                    "status": "success",
                    "message": "Tasks listed successfully",
                    "data": result
                }
            elif action == "get_task":
                task_id = request.get('task_id')
                if not task_id:
                    return {
                        "status": "error",
                        "message": "Task ID is required"
                    }
                result = self.get_task(task_id)
                return {
                    "status": "success",
                    "message": "Task retrieved successfully",
                    "data": result
                }
            elif action == "create_task":
                name = request.get('name')
                if not name:
                    return {
                        "status": "error",
                        "message": "Task name is required"
                    }
                labels = request.get('labels')
                project_id = request.get('project_id')
                data = request.get('data')
                status = request.get('status')
                result = self.create_task(name, labels, project_id, data, status)
                return {
                    "status": "success",
                    "message": "Task created successfully",
                    "data": result
                }
            elif action == "update_task":
                task_id = request.get('task_id')
                if not task_id:
                    return {
                        "status": "error",
                        "message": "Task ID is required"
                    }
                name = request.get('name')
                status = request.get('status')
                result = self.update_task(task_id, name, status)
                return {
                    "status": "success",
                    "message": "Task updated successfully",
                    "data": result
                }
            elif action == "delete_task":
                task_id = request.get('task_id')
                if not task_id:
                    return {
                        "status": "error",
                        "message": "Task ID is required"
                    }
                result = self.delete_task(task_id)
                return {
                    "status": "success",
                    "message": result["message"]
                }
            elif action == "add_labels_to_task":
                task_id = request.get('task_id')
                labels = request.get('labels')
                if not all([task_id, labels]):
                    return {
                        "status": "error",
                        "message": "Task ID and labels are required"
                    }
                result = self.add_labels_to_task(task_id, labels)
                return {
                    "status": "success",
                    "message": "Labels added to task successfully",
                    "data": result
                }
            elif action == "remove_label_from_task":
                task_id = request.get('task_id')
                label_name = request.get('label_name')
                if not all([task_id, label_name]):
                    return {
                        "status": "error",
                        "message": "Task ID and label name are required"
                    }
                result = self.remove_label_from_task(task_id, label_name)
                return {
                    "status": "success",
                    "message": "Label removed from task successfully",
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
        api = TasksAPI()
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