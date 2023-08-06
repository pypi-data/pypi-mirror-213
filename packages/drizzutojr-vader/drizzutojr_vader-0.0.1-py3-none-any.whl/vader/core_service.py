import os
import json
import requests

from .general import generate_project_name
from .exceptions import VaderGeneralException

SERVICE_URL = os.environ["CORE_SERVICE_URL"]


def get_project(app_id, boundary_id):
    url = f"{SERVICE_URL}/{app_id}/{boundary_id}/project"
    response = requests.get(url)

    if response.status_code != 200:
        project_name = generate_project_name(app_id, boundary_id)
        raise VaderGeneralException(
            f"Could not fetch project {project_name}: {str(response.content)}"
        )

    return json.loads(response.content)


def get_provisioner(name):
    url = f"{SERVICE_URL}/provisioner/{name}"
    response = requests.get(url)

    if response.status_code != 200:
        raise VaderGeneralException(
            f"Could not fetch provisioner {name}: {str(response.content)}"
        )

    return json.loads(response.content)


def get_limit(app_id, boundary_id, limit_name):
    return {}
