"""
https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/organizations-api/
"""
import os
import json
import sys
from cvat_sdk import make_client

class OrganizationsAPI:
    def __init__(self):
        self.cvat_host = os.environ.get('CVAT_HOST') or os.environ.get('CVAT_API_URL')
        self.cvat_username = os.environ.get('CVAT_USERNAME')
        self.cvat_password = os.environ.get('CVAT_PASSWORD')
        self._check_config()
        self.client = None
    
    def _check_config(self):
        if not all([self.cvat_host, self.cvat_username, self.cvat_password]):
            raise ValueError("Missing required environment variables: CVAT_HOST (or CVAT_API_URL), CVAT_USERNAME, CVAT_PASSWORD")
    
    def _connect(self):
        if not self.client:
            self.client = make_client(
                self.cvat_host,
                credentials=(self.cvat_username, self.cvat_password)
            )
    
    # Organizations API
    def list_organizations(self, filters=None):
        self._connect()
        organizations = list(self.client.organizations.list(filters=filters))
        result = []
        for org in organizations:
            result.append({
                "id": org.id,
                "name": org.name,
                "slug": org.slug,
                "owner": org.owner,
                "created_date": org.created_date.isoformat() if org.created_date else None
            })
        return result
    
    def get_organization(self, organization_id):
        self._connect()
        org = self.client.organizations.get(organization_id)
        return {
            "id": org.id,
            "name": org.name,
            "slug": org.slug,
            "owner": org.owner,
            "created_date": org.created_date.isoformat() if org.created_date else None
        }
    
    def create_organization(self, name, slug=None):
        self._connect()
        org = self.client.organizations.create(
            name=name,
            slug=slug
        )
        return {
            "id": org.id,
            "name": org.name,
            "slug": org.slug
        }
    
    def update_organization(self, organization_id, name=None, slug=None):
        self._connect()
        org = self.client.organizations.get(organization_id)
        if name:
            org.name = name
        if slug:
            org.slug = slug
        org.update()
        return {
            "id": org.id,
            "name": org.name,
            "slug": org.slug
        }
    
    def delete_organization(self, organization_id):
        self._connect()
        org = self.client.organizations.get(organization_id)
        org.delete()
        return {"message": f"Organization {organization_id} deleted successfully"}
    
    def list_organization_members(self, organization_id):
        self._connect()
        org = self.client.organizations.get(organization_id)
        members = list(org.members.list())
        result = []
        for member in members:
            result.append({
                "id": member.id,
                "username": member.username,
                "role": member.role
            })
        return result
    
    def add_organization_member(self, organization_id, user_id, role):
        self._connect()
        org = self.client.organizations.get(organization_id)
        member = org.members.add(user_id, role)
        return {
            "id": member.id,
            "username": member.username,
            "role": member.role
        }
    
    def remove_organization_member(self, organization_id, user_id):
        self._connect()
        org = self.client.organizations.get(organization_id)
        org.members.remove(user_id)
        return {"message": f"Member {user_id} removed from organization {organization_id}"}
    
    def handle_request(self, request):
        try:
            action = request.get('action')
            
            if not action:
                return {
                    "status": "error",
                    "message": "Action is required"
                }
            
            # Organizations actions
            if action == "list_organizations":
                filters = request.get('filters')
                result = self.list_organizations(filters)
                return {
                    "status": "success",
                    "message": "Organizations listed successfully",
                    "data": result
                }
            elif action == "get_organization":
                organization_id = request.get('organization_id')
                if not organization_id:
                    return {
                        "status": "error",
                        "message": "Organization ID is required"
                    }
                result = self.get_organization(organization_id)
                return {
                    "status": "success",
                    "message": "Organization retrieved successfully",
                    "data": result
                }
            elif action == "create_organization":
                name = request.get('name')
                if not name:
                    return {
                        "status": "error",
                        "message": "Organization name is required"
                    }
                slug = request.get('slug')
                result = self.create_organization(name, slug)
                return {
                    "status": "success",
                    "message": "Organization created successfully",
                    "data": result
                }
            elif action == "update_organization":
                organization_id = request.get('organization_id')
                if not organization_id:
                    return {
                        "status": "error",
                        "message": "Organization ID is required"
                    }
                name = request.get('name')
                slug = request.get('slug')
                result = self.update_organization(organization_id, name, slug)
                return {
                    "status": "success",
                    "message": "Organization updated successfully",
                    "data": result
                }
            elif action == "delete_organization":
                organization_id = request.get('organization_id')
                if not organization_id:
                    return {
                        "status": "error",
                        "message": "Organization ID is required"
                    }
                result = self.delete_organization(organization_id)
                return {
                    "status": "success",
                    "message": result["message"]
                }
            elif action == "list_organization_members":
                organization_id = request.get('organization_id')
                if not organization_id:
                    return {
                        "status": "error",
                        "message": "Organization ID is required"
                    }
                result = self.list_organization_members(organization_id)
                return {
                    "status": "success",
                    "message": "Organization members listed successfully",
                    "data": result
                }
            elif action == "add_organization_member":
                organization_id = request.get('organization_id')
                user_id = request.get('user_id')
                role = request.get('role')
                if not all([organization_id, user_id, role]):
                    return {
                        "status": "error",
                        "message": "Organization ID, user ID, and role are required"
                    }
                result = self.add_organization_member(organization_id, user_id, role)
                return {
                    "status": "success",
                    "message": "Member added to organization successfully",
                    "data": result
                }
            elif action == "remove_organization_member":
                organization_id = request.get('organization_id')
                user_id = request.get('user_id')
                if not all([organization_id, user_id]):
                    return {
                        "status": "error",
                        "message": "Organization ID and user ID are required"
                    }
                result = self.remove_organization_member(organization_id, user_id)
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
        api = OrganizationsAPI()
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