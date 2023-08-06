import argparse
import sys

from pyneoncli.clicommands import CLIProject, CLIBranch, CLIEndPoint
from pyneoncli.clilist import CLIList
from pyneoncli.neonapiexceptions import NeonAPIException, NeonTimeoutException
from pyneoncli.printer import Printer


class CLIDispatcher:

    def __init__(self) -> None:
        self._printer = Printer()

    @staticmethod
    def dispatch_list(args: argparse.Namespace):
        try:
            any_args = False
            l = CLIList(args)
            if args.all:
                l.list_all()
                any_args = False
            elif args.getkey:
                print(f"{args.apikey}")
                any_args = True
            elif args.branch_ids:
                l.list_branches_for_branch_ids(args.branch_ids)
                any_args = True
            elif args.project_ids:
                l.list_projects(args.project_ids)
                any_args = True
            elif args.project_names:
                l.list_projects_by_name(args.project_names)
                any_args = True
            elif args.projects:
                l.list_projects()
                any_args = True
            elif args.branch_ids:
                l.list_branches_for_branch_ids(args.branch_ids)
                any_args = True
            elif args.op_project_ids:
                l.list_operations(args.op_project_ids)
                any_args = True
            elif args.op_ids:
                l.list_operations_details(args.op_ids)
                any_args = True
            elif args.project_id:
                l.list_endpoints(args.project_id)
                any_args = True
            if not any_args:
                l.list_all()

        except NeonAPIException as api_error:
            print(api_error, file=sys.stderr,end="")
            if api_error.text == '{"code":"","message":"supplied credentials do not pass authentication"}':
                print("have you set NEON_API_KEY in you env or in your config file (neoncli.conf)?")
            sys.exit(1)

        except NeonTimeoutException as timeout_error:
            print(timeout_error)
            sys.exit(1)

    @staticmethod
    def dispatch_main(args: argparse.Namespace):
        pass

    @staticmethod
    def dispatch_project(args: argparse.Namespace):
        p = CLIProject(args)
        if args.create_names:
            p.create_project(args.create_names)
        if args.delete_ids:
            p.delete_projects(args.delete_ids)
        if args.delete_all:
            p.delete_all_projects()

    @staticmethod
    def dispatch_branch(args: argparse.Namespace):
        b = CLIBranch(args=args)
        if args.project_ids:
            b.create_branch(args.project_ids)
        if args.delete_ids:
            b.delete_branch(args.delete_ids)

    @staticmethod
    def dispatch_endpoint(args: argparse.Namespace):
        e = CLIEndPoint(args=args)
        if args.create_id:
            e.create_endpoint(args.create_id)
        if args.delete_id:
            e.delete_endpoint(args.delete_id)
