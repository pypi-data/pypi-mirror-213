import json

import typer

from . import utils

app = typer.Typer()


@app.command(help="To create a new static service")
def create(
    name: str = typer.Argument(..., help="Name for the service"),
    repo_owner: str = typer.Argument(..., help=("Repository Owner")),
    repo_name: str = typer.Argument(..., help=("Repository Name")),
    ref: str = typer.Argument(..., help=("Service ref name")),
    description: str = typer.Option("", help="Description for the service"),
    arguments: str = typer.Option(
        "{}", help="Docker build arguments in json string format"
    ),
):
    try:
        client = utils.read_credentials()
        arguments = json.loads(arguments)
        response = client.add_static_service(
            name=name,
            description=description,
            repo_owner=repo_owner,
            repo_name=repo_name,
            ref=ref,
            arguments=arguments,
        )
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
        pass
    else:
        utils.render_success_message(response)


@app.command(help="To remove an existing static service")
def remove(
    name: str = typer.Argument(..., help="Name of the service"),
):
    try:
        client = utils.read_credentials()
        client.delete_static_service(name)
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
        pass
    else:
        utils.render_success_message(f"Removed the static service - {name}")


@app.command(help="To fetch user's static services")
def fetch(
    name: str = typer.Argument(None, help="Name of service to fetch only that service")
):
    try:
        client = utils.read_credentials()
        if name:
            utils.render_output(client.user_static_service(name))
        else:
            utils.render_output(client.user_static_services())
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
        pass

@app.command(help="To fetch static service logs")
def logs(
    name: str = typer.Argument(None, help="Name of service to fetch only that service")
):
    try:
        client = utils.read_credentials()
        utils.render_output(client.get_static_service_docker_logs(name))
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
        pass

@app.command(help="To fetch docker image download url for service")
def docker(
    name: str = typer.Argument(None, help="Name of service to fetch only that service")
):
    try:
        client = utils.read_credentials()
        utils.render_output(client.get_docker_image_url(name))
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
        pass

