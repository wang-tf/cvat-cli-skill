# CVAT CLI Tool

A command-line tool to interact with CVAT (Computer Vision Annotation Tool) directly from the terminal, following the Claude custom skill specification. **No need to write Python scripts - use commands directly!**

## Features

- Comprehensive access to CVAT API capabilities
- Support for tasks, projects, jobs, users, and implementations management
- Configuration via environment variables
- Simple and intuitive command-line interface
- Built-in help documentation and usage examples

## Requirements

- Python 3.7+
- `cvat-sdk` package
- Claude API access (if using as a skill)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/cvat-cli.git
   cd cvat-cli
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export CVAT_HOST=https://your-cvat-instance
   export CVAT_USERNAME=your-username
   export CVAT_PASSWORD=your-password
   ```

## Usage - Command Line (Highly Recommended)

**Please use `cvat-cli.py` command-line tool, no need to write Python scripts!**

### View Help

```bash
python cvat-cli.py --help
```

### Task Management

```bash
# List all tasks
python cvat-cli.py task list

# Get task details
python cvat-cli.py task get --task-id 1

# Create a new task
python cvat-cli.py task create --name "My Task" --project-id 2

# Update a task
python cvat-cli.py task update --task-id 1 --name "New Name"

# Delete a task
python cvat-cli.py task delete --task-id 1
```

### Project Management

```bash
# List all projects
python cvat-cli.py project list

# Get project details
python cvat-cli.py project get --project-id 1

# Create a new project
python cvat-cli.py project create --name "My Project"

# Update a project
python cvat-cli.py project update --project-id 1 --name "New Name"

# Delete a project
python cvat-cli.py project delete --project-id 1
```

### Job Management

```bash
# List all jobs
python cvat-cli.py job list

# Get job details
python cvat-cli.py job get --job-id 1
```

### User Management

```bash
# List all users
python cvat-cli.py user list

# Get user details
python cvat-cli.py user get --user-id 1
```

### Implementation Management

```bash
# List all implementations
python cvat-cli.py implementation list
```

## Usage as a Claude Skill

1. Package the skill directory as a zip file
2. Upload it to Claude's skill management interface
3. Configure the skill with your CVAT_HOST, username, and password
4. When using the skill in Claude conversations, **prioritize using the command-line approach**, for example:
   ```
   Please list all CVAT tasks for me
   ```
   Claude will automatically use the `cvat-cli.py task list` command instead of writing Python scripts.

## Response Format

Command output is in JSON format with the following structure:

```json
{
  "status": "success" or "error",
  "message": "Description of the result",
  "data": "Result data (if applicable)"
}
```

## Why Use Command Line Instead of Python Scripts?

1. **Simpler and more direct**: No need to write, save, and execute Python script files
2. **Faster workflow**: Complete tasks with a single command
3. **Fewer errors**: No need to handle script file paths, imports, etc.
4. **Easier to automate**: Can be easily integrated into shell scripts and CI/CD pipelines
5. **Better user experience**: Built-in help documentation and command completion support

## Troubleshooting

- **Missing environment variables**: Ensure all required environment variables are set
- **CVAT SDK not found**: Make sure `cvat-sdk` is installed
- **Authentication errors**: Verify your CVAT_HOST, username, and password
- **API errors**: Check the `message` field in the output for error details

## License

MIT
