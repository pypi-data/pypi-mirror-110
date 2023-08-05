from fabric import task
from . import project_cmd
from tasker.utils.git import Git
from tasker.utils.user import User
from tasker.utils.email import Email
from tasker.utils.registry import Registry
from tasker.utils.project import find_project


@task
def release(c, name):
    project_paths = []
    if "project_path" in c.config:
        project_paths = [c.config.project_path]
    else:
        project_paths = c.config.project_paths
    assert type(project_paths) == list

    project_cmd.release(
        project=find_project(project_paths, name),
        git=Git(),
        user=User(c.config.editor),
        shell=c,
        registry=Registry(),
        email=Email(**c.config.release_email),
        resolve_path=c.config.resolve_path,
    )
