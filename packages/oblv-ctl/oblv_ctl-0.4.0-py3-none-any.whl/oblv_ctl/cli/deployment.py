import enum
import json

import typer

from oblv_ctl.models import CreateDeploymentInput, StaticDeploymentInput, StaticDeploymentInputInfraReqs as infra_enum, StaticDeploymentInputRegionName as region_enum

from . import utils

app = typer.Typer()

regions = ["us-east-1", "us-west-2", "eu-central-1", "eu-west-2"]


class reg(enum.Enum):
    N_Virginia = "us-east-1"
    Oregon = "us-west-2"
    Frankfurt = "eu-central-1"
    London = "eu-west-2"
    


@app.command(help="Create deployment from dynamic service")
def create(
    repo_owner: str = typer.Argument(..., help=("Repository Owner")),
    repo_name: str = typer.Argument(..., help=("Repository Name")),
    ref: str = typer.Argument(..., help=("Service ref name")),
    name: str = typer.Argument(..., help=("Deployment Name")),
    public: bool = typer.Option(
        False, "--public", help="If provided, the deployment is made public"
    ),
    is_dev: bool = typer.Option(
        False, "--is-dev", help="Sets the environment of the deployment as DEV"
    ),
    region: reg = typer.Option(
        "us-east-1",
        help='Region where enclave will be deployed. The options include ["us-east-1" (N. Virginia),  "us-west-2" (Oregon), "eu-central-1" (Frankfurt), "eu-west-2" (London)]',
    ),
    args_file: str = typer.Option(
        None, help="arguments file path for enclave deployment"
    ),
):
    try:
        client = utils.read_credentials()
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
    try:
        visibility = "public" if public else "private"
        if args_file == None:
            args_file = typer.prompt(
                "Provide the arguments file for enclave deployment "
            )
        with open(args_file, "r") as f:
            args = json.load(f)
    except FileNotFoundError as e:
        utils.render_error_message(
            'Could not find the arguments file at "' + args_file + '"'
        )
    except Exception as e:
        utils.render_error_message(str(e))
    try:
        input = CreateDeploymentInput(
            repo_owner,
            repo_name,
            "github",
            ref,
            region._value_,
            name,
            visibility,
            is_dev,
            [],
            args,
        )
        res = client.create_deployment(input)
        utils.render_success_message(
            "Deployment created with id - {}".format(res.deployment_id)
        )
    except Exception as e:
        pass


@app.command(help="To terminate a deployment")
def terminate(
    deployment_id: str = typer.Argument(..., help="Deployment Id to terminate")
):
    try:
        client = utils.read_credentials()
        client.remove_deployment(deployment_id)
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
    else:
        utils.render_info_message(
            "Terminating deployment with id {}".format(deployment_id)
        )


@app.command(
    help="To get the deployment information.\n\nIf no option is provided, complete information of the deployment is shown"
)
def info(
    deployment_id: str = typer.Argument(
        ..., help="Deployment Id for which information is requested"
    ),
    state: bool = typer.Option(
        False, "--state", help="To get the current state of deployment"
    ),
    instance: bool = typer.Option(
        False, "--instance", help="To get the instance info of deployment"
    ),
    pcrs: bool = typer.Option(False, "--pcrs", help="To get the pcrs of deployment"),
):
    try:
        client = utils.read_credentials()
        depl = client.deployment_info(deployment_id)
        if not state and not instance and not pcrs:
            utils.render_output(depl)
        else:
            resp = {}
            if state:
                resp["state"] = depl.current_state
            if pcrs:
                resp["pcr_codes"] = depl.pcr_codes
            if instance:
                resp["instance"] = depl.instance
            utils.render_output(resp)
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")


@app.command(help="To get the owned deployments")
def owned():
    try:
        client = utils.read_credentials()
        depl_l = client.deployments()
        depl = []
        for d in depl_l if depl_l != None else []:
            depl.append(
                {"deployment_id": d.deployment_id, "deployment_name": d.deployment_name}
            )
        utils.render_output(depl)
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")

@app.command(help="Create deployment from static service")
def static_create(
    name: str = typer.Argument(..., help=("Deployment Name")),
    service: str = typer.Argument(..., help="Name or id of service to create deployment from"),
    marketplace: bool = typer.Option(False, "--marketplace",help="Set if service is from marketplace"),
    users: str = typer.Option(
        ..., help="Users in json string format"
    ),
    runtime_args: str = typer.Option("", help="Runtime arguments as yaml string"),
    is_dev: bool = typer.Option(
        False, "--is-dev", help="Sets the environment of the deployment as DEV"
    ),
    region: reg = typer.Option(
        "us-east-1",
        help='Region where enclave will be deployed. The options include ["us-east-1" (N. Virginia),  "us-west-2" (Oregon), "eu-central-1" (Frankfurt), "eu-west-2" (London)]',
    ),
    infra: infra_enum = typer.Option(
        "m5.xlarge",
        help='Infra for the enclave. The options include ["c5.2xlarge", "c5.xlarge", "m5.2xlarge", "m5.4xlarge", "m5.xlarge", "r5.xlarge"]',
    ),
    
):
    try:
        client = utils.read_credentials()
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0] == utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
    if users == None:
            users = typer.prompt(
                "Provide the users json string for enclave deployment "
            )
    try:
        input = StaticDeploymentInput(
            service=service,
            deployment_name=name,
            region_name=region._value_,
            is_dev_env=is_dev,
            runtime_args=runtime_args,
            users = users,
            infra_reqs=infra._value_,
            marketplace=marketplace
        )
        res = client.create_static_service_deployment(input)
        utils.render_success_message(
            "Deployment created with id - {}".format(res.deployment_id)
        )
    except Exception as e:
        pass
    