import argparse
import sys

from pyneoncli.clicommands import CLICommands
from pyneoncli.neon import NeonProject


class CLIList(CLICommands):

    def __init__(self, args: argparse.Namespace = None) -> None:
        super().__init__(args)

    def list_all(self):
        p = None
        for p in self._api.get_projects():
            self.print_obj_id("project", p)
            for branch in self._api.get_branches(p.id):
                self.print_obj_id("branch", branch, indent=2)
                for endpoint in self._api.get_endpoints(p.id):
                    self.print_obj_id("endpoint id", endpoint, sep=": ", indent=4)
        if p is None:
            self._msg.info("No projects found")

    def list_projects(self, project_ids: list[str] = None):
        if project_ids is None:
            for p in self._api.get_projects():
                self.print_obj_id("project", p)
        elif type(project_ids) is list:
            if len(project_ids) == 0:
                for p in self._api.get_projects():
                    self._p.print(p.obj_data)
            else:
                for project_id in project_ids:
                    p = self._api.get_project(project_id)
                    self._p.print(p.obj_data)
        else:
            self._msg.error(f"Wrong argument type for list_projects: {type(project_ids)}")
            sys.exit(1)

    def list_branches_for_project(self, p: NeonProject):
        for b in self._api.get_branches(p.id):
            self.print_obj_id("branch", b)

    def list_branches_for_projects(self, project_ids: list[str]):
        for i in project_ids:
            project = self._api.get_project(i)
            self.list_branches_for_project(project)

    def list_branches_for_branch_ids(self, branch_ids: list[str]):
        for i in branch_ids:
            this_pid, this_bid = i.strip().split(":")
            p = self._api.get_project(this_pid)
            print(f"{self._p.project_id(p)}")
            self.print_obj_id("branch", self._api.get_branch_by_id(this_pid, this_bid))
            for b in self._api.get_branches(p.id):
                if this_bid == b.id:
                    self.print_obj_id("branch", b)

    def list_branch_details(self, project_id:str, branch_id:str):
        self._api.get_branch(project_id, branch_id)

    def list_operations(self, project_ids: list[str]):
        for id in project_ids:
            ops = self._api.get_operations(id)
            for op in ops:
                self._p.print(op.obj_data)

    def list_operations_details(self, op_ids: list[str]):
        for op_id in op_ids:
            project_id, operation_id = op_id.strip().split(":")
            op = self._api.get_operation(project_id, operation_id)
            self._p.print(op.obj_data)

    def list_projects_by_name(self, project_names:list[str]):
        for project in self._api.get_projects():
            if project.name in project_names:
                self.print_obj_id("project", project)
                for branch in self._api.get_branches(project.id):
                    self.print_obj_id("branch", branch, indent=2)

    def list_endpoints(self, project_id: str):
        for e in self._api.get_endpoints(project_id):
            self._p.print(e.obj_data)
