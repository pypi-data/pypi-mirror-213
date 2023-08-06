import os

import typer
from rich.text import Text

from oblv_ctl import __version__, authenticate

from . import deployment, service, utils, static_service, marketplace

app = typer.Typer(no_args_is_help=True, rich_markup_mode="markdown", help="""**Oblvious Controller v{}**   
**Oblivious Software Ltd. <oblivious.ai>**  
======
  
__Description__  

---

The Oblivious Controller is a command line tool to manage your Oblivious services.
 """.format(__version__),add_completion=False)


@app.command(help="Command to login to oblv")
def login(apikey: str):
    if apikey=="":
        apikey = typer.prompt("Kindly provide your api key ")
    try:
        client = authenticate(apikey)
        credentials = "oblivious_user_id = {}\ntoken = {}".format(client.oblivious_user_id,client.token)
        os.makedirs(os.path.dirname(utils.cred_file_path), exist_ok=True)
        with open(utils.cred_file_path,'w') as f:
            f.write(credentials)
    except Exception as e:
        utils.render_error_message(str(e))
    else:
        utils.render_success_message("Logged in")
        
@app.command(help="Command to clear and invalidate the token")
def logout():
    try:
        if os.path.exists(utils.cred_file_path):
            with open(utils.cred_file_path,'w') as f:
                f.write("")
    except FileNotFoundError as e:
        #If path not found, then the use is by default logged out
        pass
    except Exception as e:
        utils.render_error_message(str(e))
    else:
        utils.render_success_message("Logged out")
    
@app.command(help="Command to fetch the VCS accounts")
def accounts():
    try:
        client = utils.read_credentials()
        utils.render_output(client.accounts())
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0]==utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
    
@app.command(help="Command to fetch/set the Public Key")
def psk(set_key : str = typer.Option(None, help="Public key to be set")):
    try:
        client = utils.read_credentials()
        if set_key!=None:
            client.set_psk(set_key)
        else:
            utils.render_output(client.psk())
    except FileNotFoundError as e:
        utils.render_warning_message("Kindly login before performing this action")
    except Exception as e:
        if e.args[0]==utils.NO_CREDS_FOUND:
            utils.render_warning_message("Kindly login before performing this action")
    
app.add_typer(service.app, name="service", help="Commands to interact with the services")
app.add_typer(static_service.app, name="static-service", help="Commands to interact with the static services")
app.add_typer(deployment.app, name="deployment", help="Commands to interact with the deployments")
app.add_typer(marketplace.app, name="marketplace", help="Commands to interact with the marketplace services")


if __name__ == "__main__":
    app()
