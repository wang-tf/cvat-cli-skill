import os
import json
import sys
from cvat_sdk import make_client

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
                "created_date": task.created_date.isoformat() if task.created_date else None
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
            "labels": [label.name for label in task.labels],
            "data": task.data,
            "segments": [{
                "id": segment.id,
                "start_frame": segment.start_frame,
                "stop_frame": segment.stop_frame
            } for segment in task.segments]
        }
    
    def create_task(self, name, labels=None, project_id=None, data=None):
        self._connect()
        task = self.client.tasks.create(
            name=name,
            labels=labels or [{"name": "object"}],
            project_id=project_id,
            data=data or []
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
                "created_date": project.created_date.isoformat() if project.created_date else None
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
            "labels": [label.name for label in project.labels]
        }
    
    def create_project(self, name, labels=None):
        self._connect()
        project = self.client.projects.create(
            name=name,
            labels=labels or [{"name": "object"}]
        )
        return {
            "id": project.id,
            "name": project.name
        }
    
    def update_project(self, project_id, name=None):
        self._connect()
        project = self.client.projects.get(project_id)
        if name:
            project.name = name
        project.update()
        return {
            "id": project.id,
            "name": project.name
        }
    
    def delete_project(self, project_id):
        self._connect()
        project = self.client.projects.get(project_id)
        project.delete()
        return {"message": f"Project {project_id} deleted successfully"}
    
    # Jobs API
    def list_jobs(self, filters=None):
        self._connect()
        jobs = list(self.client.jobs.list(filters=filters))
        result = []
        for job in jobs:
            result.append({
                "id": job.id,
                "task_id": job.task_id,
                "status": job.status,
                "assignee": job.assignee,
                "frame_count": job.frame_count
            })
        return result
    
    def get_job(self, job_id):
        self._connect()
        job = self.client.jobs.get(job_id)
        return {
            "id": job.id,
            "task_id": job.task_id,
            "status": job.status,
            "assignee": job.assignee,
            "frame_count": job.frame_count,
            "start_frame": job.start_frame,
            "stop_frame": job.stop_frame
        }
    
    # Users API
    def list_users(self):
        self._connect()
        users = list(self.client.users.list())
        result = []
        for user in users:
            result.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
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
            "email": user.email
        }
    
    # Implementations API
    def list_implementations(self):
        self._connect()
        implementations = list(self.client.implementations.list())
        result = []
        for impl in implementations:
            result.append({
                "id": impl.id,
                "name": impl.name,
                "framework": impl.framework,
                "description": impl.description
            })
        return result
    
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
                result = self.create_task(name, labels, project_id, data)
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
            
            # Projects actions
            elif action == "list_projects":
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
                result = self.create_project(name, labels)
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
                result = self.update_project(project_id, name)
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
            
            # Jobs actions
            elif action == "list_jobs":
                filters = request.get('filters')
                result = self.list_jobs(filters)
                return {
                    "status": "success",
                    "message": "Jobs listed successfully",
                    "data": result
                }
            elif action == "get_job":
                job_id = request.get('job_id')
                if not job_id:
                    return {
                        "status": "error",
                        "message": "Job ID is required"
                    }
                result = self.get_job(job_id)
                return {
                    "status": "success",
                    "message": "Job retrieved successfully",
                    "data": result
                }
            
            # Users actions
            elif action == "list_users":
                result = self.list_users()
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
            
            # Implementations actions
            elif action == "list_implementations":
                result = self.list_implementations()
                return {
                    "status": "success",
                    "message": "Implementations listed successfully",
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