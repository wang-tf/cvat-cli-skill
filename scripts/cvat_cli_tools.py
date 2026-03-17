import os
import json
import sys
from cvat_sdk import make_client
from cvat_sdk.core.proxies.tasks import Task
from cvat_sdk.core.proxies.projects import Project

class CVATCLITools:
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
    
    def _handle_tasks_list(self, args):
        self._connect()
        tasks = list(self.client.tasks.list())
        result = []
        for task in tasks:
            result.append({
                "id": task.id,
                "name": task.name,
                "status": task.status,
                "project_id": task.project_id,
                "owner": task.owner
            })
        return {
            "stdout": json.dumps(result, indent=2),
            "stderr": "",
            "returncode": 0
        }
    
    def _handle_tasks_create(self, args):
        self._connect()
        # Parse args to get name, labels, etc.
        # This is a simplified implementation
        # For more complex scenarios, we would need to parse the args properly
        task = self.client.tasks.create(
            name="New Task",
            labels=[{"name": "person"}, {"name": "car"}]
        )
        return {
            "stdout": json.dumps({"id": task.id, "name": task.name}, indent=2),
            "stderr": "",
            "returncode": 0
        }
    
    def _handle_tasks_get(self, args):
        self._connect()
        task_id = args.strip()
        if not task_id.isdigit():
            return {
                "stdout": "",
                "stderr": "Invalid task ID",
                "returncode": 1
            }
        task = self.client.tasks.get(int(task_id))
        result = {
            "id": task.id,
            "name": task.name,
            "status": task.status,
            "project_id": task.project_id,
            "owner": task.owner,
            "labels": [label.name for label in task.labels]
        }
        return {
            "stdout": json.dumps(result, indent=2),
            "stderr": "",
            "returncode": 0
        }
    
    def _handle_projects_list(self, args):
        self._connect()
        projects = list(self.client.projects.list())
        result = []
        for project in projects:
            result.append({
                "id": project.id,
                "name": project.name,
                "owner": project.owner
            })
        return {
            "stdout": json.dumps(result, indent=2),
            "stderr": "",
            "returncode": 0
        }
    
    def _handle_projects_create(self, args):
        self._connect()
        # Parse args to get name, labels, etc.
        # This is a simplified implementation
        project = self.client.projects.create(
            name="New Project",
            labels=[{"name": "person"}, {"name": "car"}]
        )
        return {
            "stdout": json.dumps({"id": project.id, "name": project.name}, indent=2),
            "stderr": "",
            "returncode": 0
        }
    
    def _execute_command(self, command, args):
        try:
            if command == "tasks list":
                return self._handle_tasks_list(args)
            elif command == "tasks create":
                return self._handle_tasks_create(args)
            elif command.startswith("tasks get"):
                task_id = args if args else command.split(" ")[2]
                return self._handle_tasks_get(task_id)
            elif command == "projects list":
                return self._handle_projects_list(args)
            elif command == "projects create":
                return self._handle_projects_create(args)
            else:
                return {
                    "stdout": "",
                    "stderr": f"Command not supported: {command}",
                    "returncode": 1
                }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "returncode": 1
            }
    
    def handle_request(self, request):
        try:
            command = request.get('command')
            args = request.get('args', '')
            
            if not command:
                return {
                    "status": "error",
                    "message": "Command is required"
                }
            
            result = self._execute_command(command, args)
            
            if result['returncode'] == 0:
                return {
                    "status": "success",
                    "message": "Command executed successfully",
                    "data": {
                        "stdout": result['stdout'],
                        "stderr": result['stderr']
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": f"Command failed with return code {result['returncode']}",
                    "data": {
                        "stdout": result['stdout'],
                        "stderr": result['stderr']
                    }
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
        skill = CVATCLITools()
        response = skill.handle_request(request)
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