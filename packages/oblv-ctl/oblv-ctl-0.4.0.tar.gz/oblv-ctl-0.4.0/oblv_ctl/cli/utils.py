import os

from rich.console import Console

from oblv_ctl import OblvClient

from ..utils import bcolors

cred_file_path = os.path.join(os.path.expanduser('~'),'.oblv','credentials')

console = Console()

NO_CREDS_FOUND = "No credentials found"

def read_credentials():
    with open(cred_file_path,'r') as f:
        contents = f.read()
        if not contents:
            raise Exception("No credentials found")
        contents = contents.split("\n")
        for c in range(2):
            contents[c]=contents[c].split(" = ")
        client = OblvClient(oblivious_user_id=contents[0][1],token=contents[1][1])
    return client


def render_output(object):
    if type(object)==list:
        console.print_json(data=[x.to_dict() for x in object])
    elif type(object)==str:
        console.print(object)
    else:
        console.print_json(data=object.to_dict())
        
def render_success_message(message: str):
    print(
                bcolors.GREEN
                + "Success"
                + bcolors.BLACK
                + bcolors.ENDC
                + f": {message}",
            )
    
def render_warning_message(message: str):
    print(
                bcolors.YELLOW
                + "WARNING"
                + bcolors.BLACK
                + bcolors.ENDC
                + f": {message}",
            )
    
def render_error_message(message: str):
    print(
                bcolors.RED
                + "ERROR"
                + bcolors.BLACK
                + bcolors.ENDC
                + f": {message}",
            )

def render_info_message(message: str):
    print(
                bcolors.BLUE
                + "INFO"
                + bcolors.BLACK
                + bcolors.ENDC
                + f": {message}",
            )
