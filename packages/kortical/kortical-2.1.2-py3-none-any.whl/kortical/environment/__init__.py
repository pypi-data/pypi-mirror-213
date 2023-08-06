from kortical.api.project import Project
from kortical.api.environment import Environment
from kortical.helpers import format_config


def get_environment_config(format=None):
    project = Project.get_selected_project()
    environment = Environment.get_selected_environment(project)

    # Get environment config from platform
    config = environment.get_environment_config()
    return format_config(config, format)


def get_environment_name():
    project = Project.get_selected_project()
    environment = Environment.get_selected_environment(project)

    return environment.name
