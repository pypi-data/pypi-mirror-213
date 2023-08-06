import json

import typer

from . import utils

app = typer.Typer()


@app.command(help="To fetch marketplace services list")
def fetch(
    page: int = typer.Option(1, help="Page number of result"),
    per_page: int = typer.Option(10, help="Total records per page", min=2),
    repo: str = typer.Option("", help="Filter for repo of service"),
    name: str = typer.Option("", help="Filter for service name"),
):
    try:
        client = utils.read_credentials()
        utils.render_output(
            client.marketplace_services(
                page=page, per_page=per_page, name_filter=name, repo_filter=repo
            )
        )
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
        pass

@app.command(help="To request addition of service to marketplace")
def add(
    name: str = typer.Argument(None, help="Name of service to move to marketplace")
):
    try:
        client = utils.read_credentials()
        client.add_service_to_marketplace(name)
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
        pass
    else:
        utils.render_success_message("Raised request for service to be moved to marketplace")
 
@app.command(help="To remove service from marketplace")
def remove(
    name: str = typer.Argument(None, help="Name of service to remove from marketplace")
):
    try:
        client = utils.read_credentials()
        client.remove_service_from_marketplace(name)
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
        pass
    else:
        utils.render_success_message("Removed service from marketplace")
       