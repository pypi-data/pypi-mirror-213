# pyneoncli

A python package and command line tool for interaction with the [Neon](https://neon.tech) Serverless Postgres [API](https://api-docs.neon.tech/reference/getting-started-with-neon-api).

This is a work in progress and this version is incomplete. 

This version only supports the Neon V2 API. 

The program can read the NEON_API_KEY from the environment or it can he loaded from a `neoncli.conf` in your home directory or
the current working directory.

## Installation

You can install the package from PyPi using pip:
```commandline
pip install pyneoncli
```

## Operation
This will install the package and the command line tool. You can invoke the command line tool 
using the command `neoncli`. Try `neoncli --help` to see the options.

## Configuration
The program can read the NEON_API_KEY from the environment or it can he loaded from a 
a configuration file `neoncli.conf` in the home directory or the current working directory. If config
files are in both locations they will be loaded first from the home directory and then from the current
working directory. The config file is a simple text file with the following format:
```text
[DEFAULT]
api_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
You can obtain a NEON api key by logging into your NEON dashboard and visiting the 
(settings)[https://console.neon.tech/app/settings/api-keys]. Key can be issued on this screen.

## Getting Started

The program is invoked using the command `neoncli`. The program has a number of subcommands.

* `neoncli --help` - Show the help message
* `neoncli list` - List any aspect of the projects associated with the api key
* `neoncli project` - Create and delete projects
* `neoncli branch` - Create and delete branches
* `neoncli endpoint` - Create and delete endpoints

## Creating a Project

To create a project you need to specify the project name. Project names do not need to be 
unique as each project is assigned a unique ID. When a project is created the JSON representation of
the project is returned. 

```commandline
$ neoncli project --create myproject
{
    "active_time_seconds": 0,
    "branch_logical_size_limit": 204800,
    "branch_logical_size_limit_bytes": 214748364800,
    "compute_time_seconds": 0,
    "consumption_period_end": "0001-01-01T00:00:00Z",
    "consumption_period_start": "0001-01-01T00:00:00Z",
    "cpu_used_sec": 0,
    "created_at": "2023-06-07T12:52:25Z",
    "creation_source": "console",
    "data_storage_bytes_hour": 0,
    "data_transfer_bytes": 0,
    "history_retention_seconds": 604800,
    "id": "tight-wildflower-125739", <---------------------------- Project ID
    "name": "myproject",   <-------------------------------------- Project name
    "owner_id": "e426dd4a-4684-4d93-9a8d-74500641e295",
    "pg_version": 15,
    "platform_id": "aws",
    "provisioner": "k8s-pod",
    "proxy_host": "us-east-2.aws.neon.tech",
    "region_id": "aws-us-east-2",
    "store_passwords": true,
    "updated_at": "2023-06-07T12:52:25Z",
    "written_data_bytes": 0
}
```

There is a limit to the number of projects you can create. The limit is related to the 
[plan](https://neon.tech/docs/introduction/billing#neon-plans) you are on. 
If you exceed the limit you will paginate an error:

```commandline
$ neoncli project --create one_two_many
create project: one_two_many
  Status Code: 422
  Reason: Unprocessable Entity
  Text: {"code":"PROJECTS_LIMIT_EXCEEDED","message":"projects limit exceeded"}
```

### Creating multiple projects

You can create multiple projects by adding the `--create` argument more than one. 
A project will be created for each `--create` argument. 

```commandline
$ neoncli --create one --create two --create three
```

This will create three projects named `one`, `two` and `three`.

# Listing projects

To list all projects run the command `neoncli list projects`. This will return a list of all projects:

```commandline
$neoncli project --create test --create staging --create production
... (output omitted)
$ neoncli list --projects
project: production:cool-boat-193583
project: staging:round-rain-228918
project: test:broad-base-938357
```

## Neoncli Object Identifiers
Within `neoncli` we used object identifiers to refer to objects. Object identifiers are of the form:
```text
<object name>:<object id>
```
For example, the project `test` has the id `broad-base-938357`. The object identifier 
for this project is `test:broad-base-938357`. Object identifiers will be used to refer to 
projects and branches. Endpoints are a little different as they are not associated 
with a name only an ID.

# Deleting Projects
To delete a project we must refer to it by its project ID (the second part of the object identifier). Thus
to delete the project `test` we would run the command:
```commandline
$ neoncli project --delete broad-base-938357
Are you sure you want to delete project broad-base-938357? (y/n): y
{
    "active_time_seconds": 0,
    "branch_logical_size_limit": 204800,
    "branch_logical_size_limit_bytes": 214748364800,
    "compute_time_seconds": 0,
    "consumption_period_end": "0001-01-01T00:00:00Z",
    "consumption_period_start": "0001-01-01T00:00:00Z",
    "cpu_used_sec": 0,
    "created_at": "2023-06-07T13:05:45Z",
    "creation_source": "console",
    "data_storage_bytes_hour": 0,
    "data_transfer_bytes": 0,
    "history_retention_seconds": 604800,
    "id": "broad-base-938357",
    "name": "test",
    "owner_id": "e426dd4a-4684-4d93-9a8d-74500641e295",
    "pg_version": 15,
    "platform_id": "aws",
    "provisioner": "k8s-pod",
    "proxy_host": "us-east-2.aws.neon.tech",
    "region_id": "aws-us-east-2",
    "store_passwords": true,
    "updated_at": "2023-06-07T13:06:41Z",
    "written_data_bytes": 0
}
```
Note that for deletion you must confirm the deletion by typing `y` or `yes` when prompted.
If you want to proceed without confirmation you can use the `--yes` option.This is a global option for 
all commands so it must preceed the command verb. This will answer yes to all prompts. For example:
```commandline
$ neoncli --yes project --delete round-rain-228918
{
    "active_time_seconds": 0,
    "branch_logical_size_limit": 204800,
    "branch_logical_size_limit_bytes": 214748364800,
    "compute_time_seconds": 0,
    "consumption_period_end": "0001-01-01T00:00:00Z",
    "consumption_period_start": "0001-01-01T00:00:00Z",
    "cpu_used_sec": 0,
    "created_at": "2023-06-07T13:05:49Z",
    "creation_source": "console",
    "data_storage_bytes_hour": 0,
    "data_transfer_bytes": 0,
    "history_retention_seconds": 604800,
    "id": "round-rain-228918",
    "name": "staging",
    "owner_id": "e426dd4a-4684-4d93-9a8d-74500641e295",
    "pg_version": 15,
    "platform_id": "aws",
    "provisioner": "k8s-pod",
    "proxy_host": "us-east-2.aws.neon.tech",
    "region_id": "aws-us-east-2",
    "store_passwords": true,
    "updated_at": "2023-06-07T13:06:54Z",
    "written_data_bytes": 0
}
```
Use with caution as deleted projects cannot be recovered. 

# Creating Branches

From the Neon (docs on branches)[https://neon.tech/docs/introduction/branching]:
> Neon allows you to instantly branch your data in the same way that you branch your code. 
> You can quickly and cost-effectively branch your data for development, testing, and 
> various other purposes, enabling you to improve developer productivity and optimize 
> continuous integration and delivery (CI/CD) pipelines. See 
> (Branching workflows)[https://neon.tech/docs/introduction/branching#branching-workflows] for a 
> discussion of different ways you can integrate branching into your development workflows.

Branches are created from a project. To create a branch you must specify the project id. 
```commandline
$ neoncli branch --create cool-boat-193583
{
    "active_time_seconds": 0,
    "compute_time_seconds": 0,
    "cpu_used_sec": 0,
    "created_at": "2023-06-07T13:22:06Z",
    "creation_source": "console",
    "current_state": "init",
    "data_transfer_bytes": 0,
    "id": "br-white-violet-411696",
    "name": "br-white-violet-411696",
    "parent_id": "br-snowy-field-689169",
    "parent_lsn": "0/1E884F0",
    "pending_state": "ready",
    "primary": false,
    "project_id": "cool-boat-193583",
    "updated_at": "2023-06-07T13:22:06Z",
    "written_data_bytes": 0
}
```








