import click
import json

from cgc.commands.compute.compute_models import EntityList, DatabasesList
from cgc.commands.compute.compute_responses import (
    template_list_response,
    template_get_start_path_response,
    compute_restart_response,
    compute_delete_response,
)

from cgc.commands.compute.compute_utills import compute_delete_payload

from cgc.utils.prepare_headers import get_api_url_and_prepare_headers
from cgc.utils.response_utils import retrieve_and_validate_response_send_metric
from cgc.utils.click_group import CustomGroup, CustomCommand
from cgc.utils.requests_helper import call_api, EndpointTypes


@click.group(name="resource", cls=CustomGroup, hidden=True)
def resource_group():
    """
    Management of templates.
    """


@resource_group.command("list_templates", cls=CustomCommand)
def template_list():
    """Lists all available templates"""
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/list_available_templates"
    metric = "resource.template.list"
    __res = call_api(request=EndpointTypes.get, url=url, headers=headers)
    click.echo(
        template_list_response(
            retrieve_and_validate_response_send_metric(__res, metric)
        )
    )


@resource_group.command("get_start_path", cls=CustomCommand)
@click.argument(
    "template", type=click.Choice([*EntityList.get_list(), *DatabasesList.get_list()])
)
def template_get_start_path(template: str):
    """Displays start path of specified template"""
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/get_template_start_path?template_name={template}"
    metric = "resource.template.get_start_path"
    __res = call_api(request=EndpointTypes.get, url=url, headers=headers)
    click.echo(
        template_get_start_path_response(
            retrieve_and_validate_response_send_metric(__res, metric)
        )
    )


@resource_group.command("restart", cls=CustomCommand)
@click.argument("name", type=click.STRING)
def compute_restart(name: str):
    """Restarts the specified app"""
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/restart"
    metric = "resource.restart"
    __payload = {"name": name}
    __res = call_api(
        request=EndpointTypes.post,
        url=url,
        headers=headers,
        data=json.dumps(__payload),
    )
    click.echo(
        compute_restart_response(
            retrieve_and_validate_response_send_metric(__res, metric)
        )
    )


def resource_delete(name: str):
    """
    Delete an app using backend endpoint.
    \f
    :param name: name of app to delete
    :type name: str
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/delete"
    metric = "resource.delete"
    __payload = compute_delete_payload(name=name)
    __res = call_api(
        request=EndpointTypes.delete,
        url=url,
        headers=headers,
        data=json.dumps(__payload),
    )
    click.echo(
        compute_delete_response(
            retrieve_and_validate_response_send_metric(__res, metric)
        )
    )
