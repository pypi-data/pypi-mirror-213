import queue
import threading
from typing import Iterator

from pyneoncli.neonapiexceptions import NeonTimeoutException
from pyneoncli.neon import NeonProject, NeonBranch, NeonEndPoint
from pyneoncli.neonapi import NeonAPI

class ThreadedNeonAPI(NeonAPI):
    TIMEOUT_DEFAULT = 30.0  # 30 seconds

    def __init__(self, api_key: str = None, sleep_time: float = 0.1, timeout: float = TIMEOUT_DEFAULT, thread_count:int = 4) -> None:
        super().__init__(api_key=api_key, sleep_time=sleep_time, timeout=timeout)
        self._q = queue.Queue()
        self._thread_count = thread_count

    def create_project(self, project_name: str, threaded=False) -> NeonProject:
        p = super().create_project(project_name)
        if threaded:
            self._q.put(p)
        return p

    def threader(self, params:list[object], func:callable, **kwargs):
        threads = []
        thread_count = 0
        for param in params:
            t = threading.Thread(target=func, args=(param, True), daemon=True)
            threads.append(t)
            t.start()
            thread_count += 1
            if thread_count == self._thread_count:
                for t in threads:
                    t.join()
                threads = []
                thread_count = 0

        if len(threads) > 0:
            for t in threads:
                t.join()
        objects = []
        while not self._q.empty():
            objects.append(self._q.get())
        return objects

    def create_projects(self, project_names: list[str]) -> list[NeonProject] | None:
        projects: list[NeonProject] = []

        if len(project_names) == 0:
            return None
        elif len(project_names) == 1:
            projects.append(self.create_project(project_names[0]))
            return projects
        else:
            return self.threader(project_names, self.create_project)

    def delete_project(self, project_id: str) -> NeonProject:
        return super().delete_project(project_id)

    def delete_projects(self, project_ids: list[str]) -> list[NeonProject]|None:
        projects: list[NeonProject] = []

        if len(project_ids) == 0:
            return None
        elif len(project_ids) == 1:
            projects.append(self.delete_project(project_ids[0]))
            return projects
        else:
            return self.threader(project_ids, self.delete_project)
    def get_project(self, project_id: str) -> NeonProject:
        p = super().get_project(project_id)

    def get_projects_by_id(self, project_ids: list[str] = None) -> Iterator[NeonProject]:
       yield from super().get_projects_by_id(project_ids=project_ids)

    def create_branch(self, project_id: str) -> NeonBranch:
        return super().create_branch(project_id)

    def get_branch_by_id(self, project_id: str, branch_id: str) -> NeonBranch:
        return super().get_branch_by_id(project_id, branch_id)

    def get_branches(self, project_id: str) -> Iterator[NeonBranch]:
       yield from super().get_branches(project_id)

    def get_endpoints(self, project_id: str) -> Iterator[NeonEndPoint]:
        yield from super().get_endpoints(project_id)

    def create_endpoint(self, project_id: str, branch_id: str) -> NeonEndPoint:
        return super().create_endpoint(project_id, branch_id)

    def delete_endpoint(self, project_id: str, endpoint_id: str) -> NeonEndPoint:
        return super().delete_endpoint(project_id, endpoint_id)

    def get_branch(self, project_id, branch_id) -> NeonBranch:
        return super().get_branch(project_id, branch_id)

