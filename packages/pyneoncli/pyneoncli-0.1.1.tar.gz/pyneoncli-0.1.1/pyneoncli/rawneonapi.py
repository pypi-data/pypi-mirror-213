import time
from typing import Iterator

from pyneoncli.neon import NeonOperation, NeonProject, NeonBranch, NeonEndPoint
from pyneoncli.neonapiexceptions import NeonAPIException
from pyneoncli.neonliterals import NeonAPIPaths as np, NeonFunction as nf
from pyneoncli.requester import Requester


class RawNeonAPI:

    def __init__(self, api_key: str = None) -> None:
        self._api_key = api_key
        self._requester = Requester(api_key=self._api_key)

    def get_first_operation(self, project_id: str) -> NeonOperation:
        try:
            path = np.GET_OPERATIONS(project_id=project_id)
            for item in self._requester.paginate(path=path, selector=nf.operations()):
                return NeonOperation(item)
        except NeonAPIException as err:
            err.operation = "get_first_operation"
            raise err

    def get_operations(self, project_id: str) -> Iterator[NeonOperation]:
        try:
            path = np.GET_OPERATIONS( project_id=project_id)
            for item in self._requester.paginate(path=path, selector=nf.operations()):
                yield NeonOperation(item)
        except NeonAPIException as err:
            err.operation = "get_operations"
            raise err

    def get_operation(self, project_id: str, operation_id: str) -> NeonOperation:
        try:
            path = np.GET_OPERATION(project_id=project_id, operation_id=operation_id)
            return NeonOperation(self._requester.get_one(path=path, selector=nf.operation()))
        except NeonAPIException as err:
            err.operation = "get_operation"
            raise err

    def is_complete(self, project_id: str, sleep_time: float = 0.01, timeout: float = 30.0) -> bool:
        complete, _ = self.completion_time(project_id, sleep_time=sleep_time, timeout=timeout)
        return complete

    def completion_time(self, project_id: str, sleep_time: float = 0.1, timeout: float = 30.0) -> tuple[bool, float]:
        start = time.time()
        so_far = start
        while True:
            op = self.get_first_operation(project_id)
            if op.status == "finished":
                so_far = time.time() - start
                return True, so_far
            else:
                time.sleep(sleep_time)
                so_far = time.time() - start
                if so_far > timeout:
                    return False, so_far

    def create_project(self, project_name: str) -> NeonProject:
        payload = {"project": {"name": project_name}}
        try:
            data = self._requester.create(path=np.GET_PROJECTS(), payload=payload, selector=nf.project())
            return NeonProject(data=data)
        except NeonAPIException as err:
            err.operation = "create_project"
            raise err

    def delete_project(self, project_id: str) -> NeonProject:
        try:
            data = self._requester.delete(np.GET_PROJECT(project_id=project_id), selector=nf.project())
            return NeonProject(data=data)
        except NeonAPIException as err:
            err.operation = "delete_projects"
            raise err

    def count_projects(self) -> int:
        return len(list(self.get_projects()))

    def get_projects(self, batch_size: int = 20) -> Iterator[NeonProject]:
        try:
            for item in self._requester.paginate(np.GET_PROJECTS(), limit=batch_size, selector=nf.projects()):
                yield NeonProject(item)
        except NeonAPIException as err:
            err.operation = "get_projects"
            raise err

    def get_project(self, project_id: str) -> NeonProject:
        try:
            path = np.GET_PROJECT(project_id=project_id)
            data = self._requester.get_one(path=path, selector=nf.project())
            return NeonProject(data=data)
        except NeonAPIException as err:
            err.operation = "get_project"
            raise err

    def get_projects_by_id(self, project_ids: list[str] = None) -> Iterator[NeonProject]:
        try:
            if project_ids is None:
                yield from self.get_projects()
            elif not isinstance(project_ids, list):
                raise TypeError("project_ids must be a list")
            elif len(project_ids) == 0:
                yield from self.get_projects()
            else:
                for _id in project_ids:
                    yield self.get_project(_id)
        except NeonAPIException as err:
            err.operation = "get_projects_by_id"
            raise err

    def create_branch(self, project_id: str) -> NeonBranch:
        try:
            data = self._requester.POST(np.GET_BRANCHES(project_id=project_id))
            return NeonBranch(data=data)
        except NeonAPIException as err:
            err.operation = "create_branch"
            raise err

    def delete_branch(self, project_id: str, branch_id: str) -> NeonBranch:
        try:
            data = self._requester.DELETE(f"projects/{project_id}/{nf.branches}/{branch_id}")
            return NeonBranch(data=data)
        except NeonAPIException as err:
            err.operation = "delete_branch"
            raise err

    def get_branch_by_id(self, project_id: str, branch_id: str) -> NeonBranch:
        try:
            path = np.GET_BRANCH(project_id=project_id, branch_id=branch_id)
            data = self._requester.get_one(path=path, selector=nf.branch())
            return NeonBranch(data=data)
        except NeonAPIException as err:
            err.operation = "get_branch_by_id"
            raise err

    def get_branches(self, project_id: str) -> Iterator[NeonBranch]:
        try:
            path = np.GET_BRANCHES(project_id=project_id)
            return (NeonBranch(item) for item in
                    self._requester.paginate(path=path, selector=nf.branches()))
        except NeonAPIException as err:
            err.operation = "get_branches"
            raise err

    def get_endpoints(self, project_id: str) -> Iterator[NeonEndPoint]:
        try:
            path = np.ENDPOINTS( project_id=project_id)
            return (NeonEndPoint(item) for item in self._requester.paginate(path=path, selector=nf.endpoints()))
        except NeonAPIException as err:
            err.operation = "get_endpoints"
            raise err

    def create_endpoint(self, project_id: str, branch_id: str) -> NeonEndPoint:
        payload = {
            "endpoint": {
                "type": "read_write",
                "pooler_mode": "transaction",
                "branch_id": branch_id
            }
        }
        try:
            path = np.ENDPOINTS(project_id=project_id)
            data = self._requester.POST(path, data=payload)
            return NeonEndPoint(data=data)
        except NeonAPIException as err:
            err.operation = "create_endpoint"
            raise err

    def delete_endpoint(self, project_id, endpoint_id) -> NeonEndPoint:
        try:
            path =np.ENDPOINTS(project_id=project_id, endpoint_id=endpoint_id)
            data = self._requester.DELETE(path)
            return NeonEndPoint(data=data)
        except NeonAPIException as err:
            err.operation = "delete_endpoint"
            raise err

    def get_branch(self, project_id, branch_id):
        try:
            path = np.GET_BRANCH(project_id=project_id, branch_id=branch_id)
            data = self._requester.get_one(path)
            return NeonBranch(data=data)
        except NeonAPIException as err:
            err.operation = "get_branch"
            raise err
