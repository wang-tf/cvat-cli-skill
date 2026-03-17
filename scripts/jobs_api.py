import os
import json
import sys
from cvat_sdk import make_client

class JobsAPI:
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
                "owner": job.owner,
                "created_date": job.created_date.isoformat() if job.created_date else None,
                "updated_date": job.updated_date.isoformat() if job.updated_date else None,
                "frame_count": job.frame_count,
                "start_frame": job.start_frame,
                "stop_frame": job.stop_frame
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
            "owner": job.owner,
            "created_date": job.created_date.isoformat() if job.created_date else None,
            "updated_date": job.updated_date.isoformat() if job.updated_date else None,
            "frame_count": job.frame_count,
            "start_frame": job.start_frame,
            "stop_frame": job.stop_frame,
            "labels": [label.name for label in job.labels]
        }
    
    def update_job(self, job_id, status=None, assignee=None):
        self._connect()
        job = self.client.jobs.get(job_id)
        if status:
            job.status = status
        if assignee:
            job.assignee = assignee
        job.update()
        return {
            "id": job.id,
            "status": job.status,
            "assignee": job.assignee
        }
    
    def delete_job(self, job_id):
        self._connect()
        job = self.client.jobs.get(job_id)
        job.delete()
        return {"message": f"Job {job_id} deleted successfully"}
    
    def handle_request(self, request):
        try:
            action = request.get('action')
            
            if not action:
                return {
                    "status": "error",
                    "message": "Action is required"
                }
            
            # Jobs actions
            if action == "list_jobs":
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
            elif action == "update_job":
                job_id = request.get('job_id')
                if not job_id:
                    return {
                        "status": "error",
                        "message": "Job ID is required"
                    }
                status = request.get('status')
                assignee = request.get('assignee')
                result = self.update_job(job_id, status, assignee)
                return {
                    "status": "success",
                    "message": "Job updated successfully",
                    "data": result
                }
            elif action == "delete_job":
                job_id = request.get('job_id')
                if not job_id:
                    return {
                        "status": "error",
                        "message": "Job ID is required"
                    }
                result = self.delete_job(job_id)
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
        api = JobsAPI()
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