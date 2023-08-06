import sys
import argparse

from pyneoncli.neon import NeonObject
from pyneoncli.neonapi import NeonAPI
from pyneoncli.neonapiexceptions import NeonAPIException
from pyneoncli.printer import Printer
from pyneoncli.colortext import ColorText
from pyneoncli.msg import Msg


class CLICommands:

    def __init__(self, args: argparse.Namespace) -> None:
        self._args = args
        self._api_key = args.apikey
        self._api = NeonAPI(args.apikey)
        self._msg = Msg(no_color=args.nocolor)
        if args is None:
            self._p = Printer()
            self._c = ColorText()
        else:
            self._p = Printer(nocolor=args.nocolor, filters=args.fieldfilter)
            self._c = ColorText(no_color=args.nocolor)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value
        self._p = Printer(nocolor=self._args.nocolor, filters=self._args.fieldfilter)
        self._c = ColorText(no_color=self._args.nocolor)

    def print_obj_id(self, label, p:NeonObject, indent=0, sep=": ", end="\n"):
        indent = " " * indent
        name_str = None
        id_str = None

        if not isinstance(p, NeonObject):
            raise NeonAPIException("Object is not a NeonObject at print_obj_id")

        if "id" in p.obj_data:
            id_str = p.id
        if "name" in p.obj_data:
            name_str = p.name

        if name_str is None and id_str is None:
            raise NeonAPIException("No name or id found in object at print_object-Id")
        elif name_str is None:
            self._msg.kv(f"{indent}{label}", f"{self._c.yellow(id_str)}", sep=sep, end=end)
        else:
            self._msg.kv(f"{indent}{label}", f"{name_str}:{self._c.yellow(id_str)}", sep=sep, end=end)

    def report_exception(self, e:NeonAPIException, op: str, msg: str):
        self._msg.error_kv(op, msg)
        self._msg.error_kv("  Status Code", e.err.response.status_code)
        self._msg.error_kv("  Reason", e.err.response.reason)
        self._msg.error_kv("  Text", e.err.response.text)


class CLIProject(CLICommands):

    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)

    def create_one_project(self, project_name: str):
        project = self._api.create_project(project_name)
        self._p.print(project.obj_data)
        return project

    def create_project(self, project_names: list[str]) -> list[str]:
        project_ids = []
        if project_names is not None and type(project_names) is list:
            for project_name in project_names:
                try:
                    p = self.create_one_project(project_name)
                    project_ids.append(p.id)
                except NeonAPIException as e:
                    self.report_exception(e, "create project", project_name)
                    sys.exit(1)

        if len(project_ids) == 0:
            raise NeonAPIException("No projects created")
        return project_ids

    def delete_one_project(self, project_id: str, check=True):
        if check:
            resp = self._msg.prompter(msg=f"Are you sure you want to delete project {project_id}? (y/n): ",
                                      expected=["y", "Y", "yes", "Yes", "YES"],
                                      yes=self._args.yes)
            if resp:
                project = self._api.delete_project(project_id)
                self._p.print(project.obj_data)
                return project
            else:
                self._msg.warning("Aborted project deletion")
                return None
        else:
            project = self._api.delete_project(project_id)
            self._p.print(project.obj_data)
            return project

    def delete_projects(self, project_ids: list[str], check=True) -> list[str]:
        deleted_project_ids = []
        if project_ids is not None and type(project_ids) is list:
            for project_id in project_ids:
                try:
                    p = self.delete_one_project(project_id, check=check)
                    if p is not None:
                        deleted_project_ids.append(p.id)
                except NeonAPIException as e:
                    self.report_exception(e, "delete project", project_id)
        else:
            self._msg.error("You must specify a project id with --project_id for delete project")
            sys.exit(1)
        return deleted_project_ids

    def delete_all_projects(self):
        project_ids = []
        any_ids = False
        resp = self._msg.prompter(msg=f"Are you sure you want to delete all projects? (y/n): ",
                                  expected=["y", "Y", "yes", "Yes", "YES"],
                                  yes=self._args.yes)
        if resp is not None:
            for project in self._api.get_projects():
                self._api.delete_project(project.id)
                project_ids.append(project.id)
                self.print_obj_id("", project, sep="", end="")
                self._msg.green(f" deleted")
                any_ids = True
            if not any_ids:
                self._msg.info("No projects to delete")
            return project_ids
        else:
            self._msg.warning("Aborting delete all projects")
            return None


class CLIBranch(CLICommands):

    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)

    def create_one_branch(self, project_id: str):
        project = self._api.get_project(project_id)
        branch = self._api.create_branch(project.id)
        self._p.print(branch.obj_data)
        return branch

    def create_branch(self, project_ids: list[str]):
        branches = []
        for project_id in project_ids:
            branch = self.create_one_branch(project_id)
            branches.append(branch)
        return branches

    def delete_branch(self, branch_ids: list[str]):
        if branch_ids is not None and type(branch_ids) is list:
            for id in branch_ids:
                pid, bid = id.strip().split(":")
                b = self._api.delete_branch(pid, bid)
                self._p.print(b.obj_data)
        else:
            self._msg.error("You must specify a branch id with --branch_id for delete branch")
            sys.exit(1)


class CLIEndPoint(CLICommands):
    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)

    def create_endpoint(self, create_id: str):
        project_id, branch_id = create_id.strip().split(":")
        endpoint = self._api.create_endpoint(project_id, branch_id)
        self._p.print(endpoint.obj_data)
        return endpoint

    def delete_endpoint(self, delete_id: str):
        project_id, endpoint_id = delete_id.strip().split(":")
        endpoint = self._api.delete_endpoint(project_id, endpoint_id)
        self._p.print(endpoint.obj_data)
        return endpoint


