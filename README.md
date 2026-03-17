# CVAT SDK Skill

A skill to interact with CVAT (Computer Vision Annotation Tool) via CVAT SDK, following the Claude custom skill specification.

## Features

- Comprehensive access to CVAT API capabilities
- Support for tasks, projects, jobs, users, and implementations management
- Configuration via environment variables
- Proper error handling and response formatting

## Requirements

- Python 3.7+
- `cvat-sdk` package
- Claude API access

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/cvat-sdk-skill.git
   cd cvat-sdk-skill
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export CVAT_API_URL=https://your-cvat-instance/api/v1
   export CVAT_USERNAME=your-username
   export CVAT_PASSWORD=your-password
   ```

## Usage

### As a Claude Skill

1. Package the skill directory as a zip file
2. Upload it to Claude's skill management interface
3. Configure the skill with your CVAT API URL, username, and password
4. Use the skill in Claude conversations:
   ```
   @CVAT SDK Skill
   {
     "action": "list_tasks"
   }
   ```

### Local Testing

You can test the skill locally by running:

```bash
python scripts/cvat_cli_tools.py '{"action": "list_tasks"}'
```

## Supported Actions

### Tasks
- `list_tasks` - List all tasks
- `get_task` - Get task details
- `create_task` - Create a new task
- `update_task` - Update a task
- `delete_task` - Delete a task

### Projects
- `list_projects` - List all projects
- `get_project` - Get project details
- `create_project` - Create a new project
- `update_project` - Update a project
- `delete_project` - Delete a project

### Jobs
- `list_jobs` - List all jobs
- `get_job` - Get job details

### Users
- `list_users` - List all users
- `get_user` - Get user details

### Implementations
- `list_implementations` - List all implementations

### Lambda Functions
- `list_lambdas` - List all lambda functions
- `get_lambda` - Get lambda function details
- `create_lambda` - Create a new lambda function
- `update_lambda` - Update a lambda function
- `delete_lambda` - Delete a lambda function
- `upload_lambda_code` - Upload code to a lambda function

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

## License

MIT
