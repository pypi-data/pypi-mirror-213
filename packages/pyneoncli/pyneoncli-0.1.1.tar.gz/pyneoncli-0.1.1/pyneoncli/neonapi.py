from typing import Iterator

from pyneoncli.neonapiexceptions import NeonTimeoutException
from pyneoncli.neon import NeonProject, NeonBranch, NeonEndPoint
from pyneoncli.rawneonapi import RawNeonAPI


class NeonAPI(RawNeonAPI):
    TIMEOUT_DEFAULT = 30.0  # 30 seconds

    def __init__(self, api_key: str | None = None, sleep_time: float = 0.1, timeout: float = TIMEOUT_DEFAULT) -> None:
        self._api_key = api_key
        self._timeout = timeout
        self._sleep_time = sleep_time
        super().__init__(api_key=self._api_key)

    def create_project(self, project_name: str) -> NeonProject:
        p = super().create_project(project_name)
        if self.is_complete(project_id=p.id, sleep_time=self._sleep_time, timeout=self._timeout):
            return p
        else:
            raise NeonTimeoutException(f"Project creation for {project_name} timed out after {self._timeout} seconds")

    def delete_project(self, project_id: str) -> NeonProject:
        return super().delete_project(project_id)

    def get_project(self, project_id: str) -> NeonProject:
        p = super().get_project(project_id)
        if self.is_complete(project_id=p.id, sleep_time=self._sleep_time, timeout=self._timeout):
            return p
        else:
            raise NeonTimeoutException(f"get_project timed out after {self._timeout} seconds for {p.id}")

    def get_projects_by_id(self, project_ids: list[str] = None) -> Iterator[NeonProject]:
        for p in super().get_projects_by_id(project_ids=project_ids):
            if self.is_complete(project_id=p.id, sleep_time=self._sleep_time, timeout=self._timeout):
                yield p
            else:
                raise NeonTimeoutException(f"get_project timed out after {self._timeout} seconds for {p.id}")

    def create_branch(self, project_id: str) -> NeonBranch:
        b = super().create_branch(project_id)
        if self.is_complete(project_id=project_id, sleep_time=self._sleep_time, timeout=self._timeout):
            return b
        else:
            raise NeonTimeoutException(f"Branch creation for {project_id} timed out after {self._timeout} seconds")

    def get_branch_by_id(self, project_id: str, branch_id: str) -> NeonBranch:
        b = super().get_branch_by_id(project_id, branch_id)
        if self.is_complete(project_id=project_id, sleep_time=self._sleep_time, timeout=self._timeout):
            return b
        else:
            raise NeonTimeoutException(f"get_branch_by_id timed out after {self._timeout} seconds for {b.id}")

    def get_branches(self, project_id: str) -> Iterator[NeonBranch]:
        for b in super().get_branches(project_id):
            if self.is_complete(project_id=project_id, sleep_time=self._sleep_time, timeout=self._timeout):
                yield b
            else:
                raise NeonTimeoutException(f"get_branches timed out after {self._timeout} seconds for {b.id}")

    def get_endpoints(self, project_id: str) -> Iterator[NeonEndPoint]:
        for e in super().get_endpoints(project_id):
            if self.is_complete(project_id=project_id, sleep_time=self._sleep_time, timeout=self._timeout):
                yield e
            else:
                raise NeonTimeoutException(f"get_endpoints timed out after {self._timeout} seconds for {e.id}")
        pass

    def create_endpoint(self, project_id: str, branch_id: str) -> NeonEndPoint:
        e = super().create_endpoint(project_id, branch_id)
        if self.is_complete(project_id=project_id, sleep_time=self._sleep_time, timeout=self._timeout):
            return e
        else:
            raise NeonTimeoutException(f"create_endpoint timed out after {self._timeout} seconds for {e.id}")

    def delete_endpoint(self, project_id: str, endpoint_id: str) -> NeonEndPoint:
        e = super().delete_endpoint(project_id, endpoint_id)
        if self.is_complete(project_id=project_id, sleep_time=self._sleep_time, timeout=self._timeout):
            return e
        else:
            raise NeonTimeoutException(f"delete_endpoint timed out after {self._timeout} seconds for {e.id}")

    def get_branch(self, project_id, branch_id):
        bd = (super().get_branch(project_id, branch_id))
        if self.is_complete(project_id=project_id, sleep_time=self._sleep_time, timeout=self._timeout):
            return bd
        else:
            raise NeonTimeoutException(f"get_branch timed out after {self._timeout} seconds for {bd.id}")
