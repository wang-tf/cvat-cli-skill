---
name: CVAT SDK Skill
description: A skill to interact with CVAT (Computer Vision Annotation Tool) via CVAT SDK. Use this skill to manage annotation tasks, projects, jobs, users, and implementations.
dependencies:
  - cvat-sdk
scripts:
  - scripts/cvat_cli_tools.py
  - scripts/lambda_api.py
  - scripts/projects_api.py
  - scripts/tasks_api.py
  - scripts/cloudstorages_api.py
  - scripts/events_api.py
  - scripts/jobs_api.py
  - scripts/users_api.py
  - scripts/organizations_api.py
---

# CVAT SDK Skill

## Overview

This skill allows you to interact with CVAT (Computer Vision Annotation Tool) directly through the CVAT SDK. It provides comprehensive access to CVAT's API capabilities, including managing tasks, projects, jobs, users, and implementations.

## Configuration

The skill requires the following environment variables to be set:

- `CVAT_API_URL`: The URL of your CVAT API instance (e.g., https://your-cvat-instance/api/v1)
- `CVAT_USERNAME`: Your CVAT username
- `CVAT_PASSWORD`: Your CVAT password

## Usage

To use this skill, provide a JSON object with the following parameters:

- `action`: The API action to perform (required)
- Additional parameters specific to the action

### Supported Actions

#### Tasks
- `list_tasks`: List all tasks
  - Optional: `filters` - Filter criteria
- `get_task`: Get task details
  - Required: `task_id` - Task ID
- `create_task`: Create a new task
  - Required: `name` - Task name
  - Optional: `labels` - List of labels
  - Optional: `project_id` - Project ID
  - Optional: `data` - List of data URLs
- `update_task`: Update a task
  - Required: `task_id` - Task ID
  - Optional: `name` - New task name
  - Optional: `status` - New task status
- `delete_task`: Delete a task
  - Required: `task_id` - Task ID

#### Projects
- `list_projects`: List all projects
  - Optional: `filters` - Filter criteria
- `get_project`: Get project details
  - Required: `project_id` - Project ID
- `create_project`: Create a new project
  - Required: `name` - Project name
  - Optional: `labels` - List of labels
- `update_project`: Update a project
  - Required: `project_id` - Project ID
  - Optional: `name` - New project name
- `delete_project`: Delete a project
  - Required: `project_id` - Project ID

#### Jobs
- `list_jobs`: List all jobs
  - Optional: `filters` - Filter criteria
- `get_job`: Get job details
  - Required: `job_id` - Job ID

#### Users
- `list_users`: List all users
- `get_user`: Get user details
  - Required: `user_id` - User ID

#### Implementations
- `list_implementations`: List all implementations

#### Lambda Functions
- `list_lambdas`: List all lambda functions
  - Optional: `filters` - Filter criteria
- `get_lambda`: Get lambda function details
  - Required: `lambda_id` - Lambda function ID
- `create_lambda`: Create a new lambda function
  - Required: `name` - Lambda function name
  - Required: `runtime` - Runtime environment
  - Required: `entrypoint` - Entrypoint function
  - Optional: `description` - Description
  - Optional: `memory_limit` - Memory limit (default: 128)
  - Optional: `timeout` - Timeout in seconds (default: 30)
- `update_lambda`: Update a lambda function
  - Required: `lambda_id` - Lambda function ID
  - Optional: `name` - New name
  - Optional: `description` - New description
  - Optional: `memory_limit` - New memory limit
  - Optional: `timeout` - New timeout
- `delete_lambda`: Delete a lambda function
  - Required: `lambda_id` - Lambda function ID
- `upload_lambda_code`: Upload code to a lambda function
  - Required: `lambda_id` - Lambda function ID
  - Required: `code_path` - Path to code zip file

### Examples

#### List tasks
```json
{
  "action": "list_tasks"
}
```

#### Get task details
```json
{
  "action": "get_task",
  "task_id": 1
}
```

#### Create a project
```json
{
  "action": "create_project",
  "name": "New Project",
  "labels": [{"name": "person"}, {"name": "car"}]
}
```

#### List lambda functions
```json
{
  "action": "list_lambdas"
}
```

#### Create a lambda function
```json
{
  "action": "create_lambda",
  "name": "My Lambda",
  "runtime": "python3.8",
  "entrypoint": "handler.main",
  "description": "Test lambda function",
  "memory_limit": 256,
  "timeout": 60
}
```

## Response Format

The skill returns responses in JSON format with the following structure:

```json
{
  "status": "success" or "error",
  "message": "Description of the result",
  "data": "Result data (if applicable)"
}
```

## Troubleshooting

- **Missing environment variables**: Ensure all required environment variables are set
- **CVAT SDK not found**: Make sure `cvat-sdk` is installed
- **Authentication errors**: Verify your CVAT API URL, username, and password
- **API errors**: Check the `message` field in the response for error details
