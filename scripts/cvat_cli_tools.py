import os
import subprocess
import json
import sys

class CVATCLITools:
    def __init__(self):
        self.cvat_api_url = os.environ.get('CVAT_API_URL')
        self.cvat_username = os.environ.get('CVAT_USERNAME')
        self.cvat_password = os.environ.get('CVAT_PASSWORD')
        self._check_config()
    
    def _check_config(self):
        if not all([self.cvat_api_url, self.cvat_username, self.cvat_password]):
            raise ValueError("Missing required environment variables: CVAT_API_URL, CVAT_USERNAME, CVAT_PASSWORD")
    
    def _build_command(self, command, args):
        base_cmd = ["cvat-cli"]
        base_cmd.extend(command.split())
        if args:
            base_cmd.extend(args.split())
        return base_cmd
    
    def _execute_command(self, cmd):
        try:
            # Set environment variables for CVAT CLI
            env = os.environ.copy()
            env['CVAT_API_URL'] = self.cvat_api_url
            env['CVAT_USERNAME'] = self.cvat_username
            env['CVAT_PASSWORD'] = self.cvat_password
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env
            )
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
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
            
            cmd = self._build_command(command, args)
            result = self._execute_command(cmd)
            
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