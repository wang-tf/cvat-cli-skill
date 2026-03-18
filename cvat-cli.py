#!/usr/bin/env python3
import argparse
import sys
import json
from scripts.base import CVATBase, print_response


class CVATCLI(CVATBase):
    def __init__(self):
        super().__init__()

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

    def list_jobs(self, filters=None):
        self._connect()
        jobs = list(self.client.jobs.list(filters=filters))
        result = []
        for job in jobs:
            result.append({
                "id": job.id,
                "task_id": job.task_id,
                "status": job.status,
                "assignee": job.assignee
            })
        return result

    def get_job(self, job_id):
        self._connect()
        job = self.client.jobs.get(job_id)
        return {
            "id": job.id,
            "task_id": job.task_id,
            "status": job.status,
            "assignee": job.assignee
        }

    def list_users(self):
        self._connect()
        users = list(self.client.users.list())
        result = []
        for user in users:
            result.append({
                "id": user.id,
                "username": user.username,
                "email": user.email
            })
        return result

    def get_user(self, user_id):
        self._connect()
        user = self.client.users.get(user_id)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }

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


def main():
    parser = argparse.ArgumentParser(
        description="CVAT CLI Tool - 直接使用命令行与 CVAT 交互，无需编写 Python 脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列出所有任务
  cvat-cli task list
  
  # 获取任务详情
  cvat-cli task get --task-id 1
  
  # 创建任务
  cvat-cli task create --name "My Task" --project-id 2
  
  # 列出所有项目
  cvat-cli project list
  
  # 获取项目详情
  cvat-cli project get --project-id 1
  
  # 创建项目
  cvat-cli project create --name "My Project"
  
  # 列出作业
  cvat-cli job list
  
  # 列出用户
  cvat-cli user list
  
  # 列出实现
  cvat-cli implementation list
        """
    )

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    task_parser = subparsers.add_parser("task", help="任务管理")
    task_subparsers = task_parser.add_subparsers(title="Task Commands", dest="subcommand")

    task_list_parser = task_subparsers.add_parser("list", help="列出所有任务")
    task_list_parser.add_argument("--filters", help="过滤条件 (JSON 格式)")

    task_get_parser = task_subparsers.add_parser("get", help="获取任务详情")
    task_get_parser.add_argument("--task-id", required=True, type=int, help="任务 ID")

    task_create_parser = task_subparsers.add_parser("create", help="创建新任务")
    task_create_parser.add_argument("--name", required=True, help="任务名称")
    task_create_parser.add_argument("--labels", help="标签 (JSON 格式列表)")
    task_create_parser.add_argument("--project-id", type=int, help="项目 ID")
    task_create_parser.add_argument("--data", help="数据 (JSON 格式列表)")
    task_create_parser.add_argument("--status", help="任务状态")

    task_update_parser = task_subparsers.add_parser("update", help="更新任务")
    task_update_parser.add_argument("--task-id", required=True, type=int, help="任务 ID")
    task_update_parser.add_argument("--name", help="新任务名称")
    task_update_parser.add_argument("--status", help="新任务状态")

    task_delete_parser = task_subparsers.add_parser("delete", help="删除任务")
    task_delete_parser.add_argument("--task-id", required=True, type=int, help="任务 ID")

    project_parser = subparsers.add_parser("project", help="项目管理")
    project_subparsers = project_parser.add_subparsers(title="Project Commands", dest="subcommand")

    project_list_parser = project_subparsers.add_parser("list", help="列出所有项目")
    project_list_parser.add_argument("--filters", help="过滤条件 (JSON 格式)")

    project_get_parser = project_subparsers.add_parser("get", help="获取项目详情")
    project_get_parser.add_argument("--project-id", required=True, type=int, help="项目 ID")

    project_create_parser = project_subparsers.add_parser("create", help="创建新项目")
    project_create_parser.add_argument("--name", required=True, help="项目名称")
    project_create_parser.add_argument("--labels", help="标签 (JSON 格式列表)")
    project_create_parser.add_argument("--status", help="项目状态")

    project_update_parser = project_subparsers.add_parser("update", help="更新项目")
    project_update_parser.add_argument("--project-id", required=True, type=int, help="项目 ID")
    project_update_parser.add_argument("--name", help="新项目名称")
    project_update_parser.add_argument("--status", help="新项目状态")

    project_delete_parser = project_subparsers.add_parser("delete", help="删除项目")
    project_delete_parser.add_argument("--project-id", required=True, type=int, help="项目 ID")

    job_parser = subparsers.add_parser("job", help="作业管理")
    job_subparsers = job_parser.add_subparsers(title="Job Commands", dest="subcommand")

    job_list_parser = job_subparsers.add_parser("list", help="列出所有作业")
    job_list_parser.add_argument("--filters", help="过滤条件 (JSON 格式)")

    job_get_parser = job_subparsers.add_parser("get", help="获取作业详情")
    job_get_parser.add_argument("--job-id", required=True, type=int, help="作业 ID")

    user_parser = subparsers.add_parser("user", help="用户管理")
    user_subparsers = user_parser.add_subparsers(title="User Commands", dest="subcommand")

    user_list_parser = user_subparsers.add_parser("list", help="列出所有用户")

    user_get_parser = user_subparsers.add_parser("get", help="获取用户详情")
    user_get_parser.add_argument("--user-id", required=True, type=int, help="用户 ID")

    impl_parser = subparsers.add_parser("implementation", help="实现管理")
    impl_subparsers = impl_parser.add_subparsers(title="Implementation Commands", dest="subcommand")

    impl_list_parser = impl_subparsers.add_parser("list", help="列出所有实现")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        cli = CVATCLI()

        if args.command == "task":
            if args.subcommand == "list":
                filters = json.loads(args.filters) if args.filters else None
                result = cli.list_tasks(filters)
                print_response(cli.success_response("Tasks listed successfully", result))
            elif args.subcommand == "get":
                result = cli.get_task(args.task_id)
                print_response(cli.success_response("Task retrieved successfully", result))
            elif args.subcommand == "create":
                labels = json.loads(args.labels) if args.labels else None
                data = json.loads(args.data) if args.data else None
                result = cli.create_task(args.name, labels, args.project_id, data, args.status)
                print_response(cli.success_response("Task created successfully", result))
            elif args.subcommand == "update":
                result = cli.update_task(args.task_id, args.name, args.status)
                print_response(cli.success_response("Task updated successfully", result))
            elif args.subcommand == "delete":
                result = cli.delete_task(args.task_id)
                print_response(cli.success_response(result["message"]))
        elif args.command == "project":
            if args.subcommand == "list":
                filters = json.loads(args.filters) if args.filters else None
                result = cli.list_projects(filters)
                print_response(cli.success_response("Projects listed successfully", result))
            elif args.subcommand == "get":
                result = cli.get_project(args.project_id)
                print_response(cli.success_response("Project retrieved successfully", result))
            elif args.subcommand == "create":
                labels = json.loads(args.labels) if args.labels else None
                result = cli.create_project(args.name, labels, args.status)
                print_response(cli.success_response("Project created successfully", result))
            elif args.subcommand == "update":
                result = cli.update_project(args.project_id, args.name, args.status)
                print_response(cli.success_response("Project updated successfully", result))
            elif args.subcommand == "delete":
                result = cli.delete_project(args.project_id)
                print_response(cli.success_response(result["message"]))
        elif args.command == "job":
            if args.subcommand == "list":
                filters = json.loads(args.filters) if args.filters else None
                result = cli.list_jobs(filters)
                print_response(cli.success_response("Jobs listed successfully", result))
            elif args.subcommand == "get":
                result = cli.get_job(args.job_id)
                print_response(cli.success_response("Job retrieved successfully", result))
        elif args.command == "user":
            if args.subcommand == "list":
                result = cli.list_users()
                print_response(cli.success_response("Users listed successfully", result))
            elif args.subcommand == "get":
                result = cli.get_user(args.user_id)
                print_response(cli.success_response("User retrieved successfully", result))
        elif args.command == "implementation":
            if args.subcommand == "list":
                result = cli.list_implementations()
                print_response(cli.success_response("Implementations listed successfully", result))
    except Exception as e:
        print_response({"status": "error", "message": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
