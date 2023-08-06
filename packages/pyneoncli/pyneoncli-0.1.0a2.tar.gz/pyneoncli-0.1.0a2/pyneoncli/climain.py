import argparse
import os
import sys
from configparser import ConfigParser

from pyneoncli.clidispatcher import CLIDispatcher
from pyneoncli.configfile import ConfigFileDefaults
from pyneoncli.msg import Msg
from pyneoncli.version import __VERSION__

NEON_API_KEY = None

epilog = f'''
use neoncli list  -h for more information on the list command
use neoncli branch  -h for more information on the branch command
use neoncli project -h for more information on the project command

Version : {__VERSION__}
'''


def main():

    env_api_key = os.getenv("NEON_API_KEY")
    cfg_files = ConfigFileDefaults()
    cfg = ConfigParser()
    cfg.read(cfg_files.config_file_list)
    default_project_id = cfg['DEFAULT']['project_id'] if 'DEFAULT' in cfg and 'project_id' in cfg['DEFAULT'] else None
    api_key = cfg['DEFAULT']['api_key'] if 'DEFAULT' in cfg and 'api_key' in cfg['DEFAULT'] else env_api_key
    #print(f"project id: {default_project_id}, api_key: {api_key}")

    parser = argparse.ArgumentParser(description='neoncli -  neon command line client',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=epilog)
    parser.add_argument('--apikey', type=str, default=api_key,
                        help='Specify NEON API Key (env NEON_API_KEY)')
    parser.add_argument("--version", action="version", version=f"neoncli {__VERSION__}")
    parser.add_argument("--nocolor", action="store_true", default=False, help="Turn off Color output")
    parser.add_argument('--yes', action="store_true", default=False, help='Answer yes to all prompts')

    parser.add_argument( '-f', '--fieldfilter', action="append", type=str, help='Enter field values to filter results on')
    parser.set_defaults(func=CLIDispatcher.dispatch_main)

    subparsers = parser.add_subparsers(dest='command', description='Invoke a specific neon command',
                                       help='e.g. neoncli list will list all projects')

    # List
    list_parser = subparsers.add_parser('list', help='List Neon objects')
    list_parser.add_argument('-k', '--getkey', action="store_true", default=False, help='list NEON API Key')
    list_parser.add_argument('-a', '--all', action="store_true", default=False, help='List all objects')
    list_parser.add_argument('-p', '--projects', action='store_true', default=False, help='list projects')
    list_parser.add_argument('-n', '--project_name', action='append', dest="project_names",
                             help='list all projects by project name')
    list_parser.add_argument('-b', '--branches', action="append", dest="project_ids",
                             help='List branches associated with project_id(s)')
    list_parser.add_argument('-pi', '--project_id', action="append", dest="project_ids",  type=str,
                             help='List projects specificed by project_id')
    list_parser.add_argument('-bi', '--branch_id', action="append", dest="branch_ids",  type=str,
                             help='List branches specified by project_id:branch_id')
    list_parser.add_argument('-o', '--operations', action="append", dest="op_project_ids",
                             help='List operations associated with project_id(s)')
    list_parser.add_argument('-d', '--operation_details', action="append", dest="op_ids",
                             help='Get operation details for project_id:operation_id')
    list_parser.add_argument('-e', '--endpoints', type=str, dest="project_id",
                             help='list endpoints for the specified project_id')
    list_parser.set_defaults(func=CLIDispatcher.dispatch_list)

    # Projects
    project_parser = subparsers.add_parser('project', help='Create and delete Neon projects')
    project_parser.add_argument('-c', '--create', action="append", dest="create_names", type=str,  help='create project')
    project_parser.add_argument('-d', '--delete', action="append", dest="delete_ids",  type=str, help='delete project')
    project_parser.add_argument('--delete_all', action="store_true", default=False,  help='delete all projects')

    project_parser.set_defaults(func=CLIDispatcher.dispatch_project)

    # Branches
    branch_parser = subparsers.add_parser('branch', help='create and delete Neon branches')
    branch_parser.add_argument('-c', '--create', action="append",  dest="project_ids", type=str, help='create branch on the project specified by project id')
    branch_parser.add_argument('-d', '--delete', action="append", dest="delete_ids", type=str,  help='delete branches specified by project_id:branch_id')
    branch_parser.add_argument('--delete_all', action="store_true", default=False,  help='delete all branches')

    branch_parser.set_defaults(func=CLIDispatcher.dispatch_branch)

    #endpoints
    endpoint_parser = subparsers.add_parser('endpoint', help='create and delete Neon endpoints')
    endpoint_parser.add_argument('-c', '--create',  dest="create_id", type=str,
                                 help='create endpoint on the project specified by project_id:branch_id')
    endpoint_parser.add_argument('-d', '--delete',  dest="delete_id", type=str,
                                 help='delete endpoints specified by project_id:endpoint_id')

    endpoint_parser.set_defaults(func=CLIDispatcher.dispatch_endpoint)

    msg = None
    try:
        args = parser.parse_args()
        msg = Msg(args.nocolor)
        args.func(args)
    except KeyboardInterrupt:
        print("")
        msg.warning("Exiting...Ctrl-C detected")

    except Exception as e:
        msg.error(f"{e}")
        sys.exit(1)
if __name__ == '__main__':
    main()
