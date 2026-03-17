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
