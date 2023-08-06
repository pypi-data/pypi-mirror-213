import queue
import threading
from multiprocessing.pool import ThreadPool

from pyneoncli.neon import NeonProject
from pyneoncli.neonapi import NeonAPI


class ThreadedCreate:

    def __init__(self, api_key=str) -> None:
        self._q = queue.Queue()
        self._api = NeonAPI(api_key)

    def create_project(self, project_name: str, threaded=False) -> NeonProject:
        project = self._api.create_project(project_name)
        if threaded:
            self._q.put(project)
        return project

    def create_projects(self, project_names: list[str]) -> list[NeonProject]:
        projects: list[NeonProject] = []
        threads: list[threading.Thread] = []

        if len(project_names) == 0:
            raise ValueError("project_names must contain at least one project name")
        elif len(project_names) == 1:
            projects.append(self.create_project(project_names[0]))
            return projects
        else:
            for i, project_name in enumerate(project_names, 1):
                t = threading.Thread(target=self.create_project, args=(project_name, True), daemon=True)
                threads.append(t)
                t.start()
            for t in threads:
                t.join()

            while not self._q.empty():
                projects.append(self._q.get())
        return projects
