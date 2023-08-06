import ssl
from typing import Dict, Union

import attr

from .config import URL


@attr.s(auto_attribs=True, repr=False)
class Client:
    """A class for keeping track of data related to the API"""
        
    cookies: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    headers: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    timeout: float = attr.ib(50.0, kw_only=True)
    verify_ssl: Union[str, bool, ssl.SSLContext] = attr.ib(True, kw_only=True)
    
    @property
    def base_url(self):
        return URL

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in all endpoints"""
        return {**self.headers}

    def with_headers(self, headers: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        return attr.evolve(self, headers={**self.headers, **headers})

    def get_cookies(self) -> Dict[str, str]:
        return {**self.cookies}

    def with_cookies(self, cookies: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        return attr.evolve(self, cookies={**self.cookies, **cookies})

    def get_timeout(self) -> float:
        return self.timeout

    def with_timeout(self, timeout: float) -> "Client":
        """Get a new client matching this one with a new timeout (in seconds)"""
        return attr.evolve(self, timeout=timeout)


@attr.s(auto_attribs=True, repr=False)
class AuthenticatedClient(Client):
    """A Client which has been authenticated for use on secured endpoints"""

    def __init__(self):
        super()
    token: str

    oblivious_user_id: str

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in authenticated endpoints"""
        return {"AuthorizationToken": f"{self.token}", **self.headers}
