from oblv_ctl.exceptions import BadRequestError
from .oblv_client import OblvClient
from .api.auth import authenticate_key_login_apikey_post
from .models import APIKey
from .client import Client

def authenticate(apikey: str):
    response = authenticate_key_login_apikey_post.sync(client=Client(), json_body=APIKey(apikey))
    return OblvClient(response.token,response.user_id)
