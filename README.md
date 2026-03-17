# CVAT CLI Skill

A skill to interact with CVAT (Computer Vision Annotation Tool) via CLI, following the Claude custom skill specification.

## Features

- Execute CVAT CLI commands directly from Claude
- Support for all CVAT CLI commands and arguments
- Configuration via environment variables
- Proper error handling and response formatting

## Requirements

- Python 3.7+
- `cvat-sdk` package
- Claude API access

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/cvat-cli-skill.git
   cd cvat-cli-skill
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
   @CVAT CLI Skill
   {
     "command": "tasks list",
     "args": "--page_size 10"
   }
   ```

### Local Testing

You can test the skill locally by running:

```bash
python main.py '{"command": "tasks list", "args": "--page_size 10"}'
```

## Command Reference

This skill supports all CVAT CLI commands. Some common commands include:

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

## License

MIT
