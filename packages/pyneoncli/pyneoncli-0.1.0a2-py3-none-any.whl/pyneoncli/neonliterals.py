from enum import Enum


class NeonFunction(Enum):
    projects = "projects"
    branches = "branches"
    operations = "operations"
    endpoints = "endpoints"
    project = "project"
    branch = "branch"
    endpoint = "endpoint"
    operation = "operation"

    def __str__(self) -> str:
        return self.value

    def __call__(self):
        return self.value


class NeonAPIPaths(Enum):
    BASE_URL_V2     = "https://console.neon.tech/api/v2/"
    GET_PROJECTS    = f"{BASE_URL_V2}projects"
    GET_PROJECT     = f"{BASE_URL_V2}projects/{{project_id}}"
    GET_BRANCHES    = f"{BASE_URL_V2}projects/{{project_id}}/branches"
    GET_BRANCH      = f"{BASE_URL_V2}projects/{{project_id}}/branches/{{branch_id}}"
    GET_OPERATIONS  = f"{BASE_URL_V2}projects/{{project_id}}/operations"
    GET_OPERATION   = f"{BASE_URL_V2}projects/{{project_id}}/operations/{{operation_id}}"
    ENDPOINTS       = f"{BASE_URL_V2}projects/{{project_id}}/endpoints"
    GET_ENDPOINT    = f"{BASE_URL_V2}projects/{{project_id}}/endpoints/{{endpoint_id}}"

    #
    # Use as f(NeonAPIPaths.PROJECTS, project_id="1234")

    def __str__(self):
        return self.value

    def __call__(self, **kwargs):
        return self.value.format(**kwargs)



