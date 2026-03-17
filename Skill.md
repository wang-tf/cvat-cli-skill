---
name: CVAT CLI Skill
description: A skill to interact with CVAT (Computer Vision Annotation Tool) via CLI. Use this skill to execute CVAT CLI commands and manage annotation tasks.
dependencies:
  - cvat-sdk
scripts:
  - scripts/cvat_cli_tools.py
---

# CVAT CLI Skill

## Overview

This skill allows you to execute CVAT (Computer Vision Annotation Tool) CLI commands directly from Claude. It supports all CVAT CLI commands and arguments, providing a seamless way to manage your annotation tasks.

## Configuration

The skill requires the following environment variables to be set:

- `CVAT_API_URL`: The URL of your CVAT API instance (e.g., https://your-cvat-instance/api/v1)
- `CVAT_USERNAME`: Your CVAT username
- `CVAT_PASSWORD`: Your CVAT password

## Usage

To use this skill, provide a JSON object with the following parameters:

- `command`: The CVAT CLI command to execute (required)
- `args`: Additional arguments for the command (optional)

### Example

```json
{
  "command": "tasks list",
  "args": "--page_size 10"
}
```

## Supported Commands

This skill supports all CVAT CLI commands, including:

- `tasks list` - List all tasks
- `tasks create` - Create a new task
- `tasks get` - Get task details
- `projects list` - List all projects
- `projects create` - Create a new project

For a complete list of commands, run `cvat-cli --help`.

## Response Format

The skill returns responses in JSON format with the following structure:

```json
{
  "status": "success" or "error",
  "message": "Description of the result",
  "data": {
    "stdout": "Command output",
    "stderr": "Command errors (if any)"
  }
}
```

## Troubleshooting

- **Missing environment variables**: Ensure all required environment variables are set
- **CVAT CLI not found**: Make sure `cvat-cli` is installed and in your PATH
- **Authentication errors**: Verify your CVAT API URL, username, and password
- **Command errors**: Check the `stderr` field in the response for error details
