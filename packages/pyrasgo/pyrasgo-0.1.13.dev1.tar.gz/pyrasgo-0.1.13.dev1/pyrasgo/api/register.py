import requests
import os

from pyrasgo.api.error import APIError
from pyrasgo.api.session import Environment
from pyrasgo.schemas.user import UserRegistration, UserLogin
from pyrasgo.utils.monitoring import track_usage

class Register:

    @track_usage
    def login(self, payload: UserLogin):
        url = self._url(resource=f"/pyrasgo-login", api_version=1)
        response = requests.post(url, json=payload.__dict__)
        status_code = response.status_code
        if status_code == 200:
            return response.json()
        if status_code == 401 or status_code == 403:
            raise APIError(f"Invalid Login Credentials")
        elif status_code == 400:
            raise APIError("API Key Expired. Contact support or verify ")

    @track_usage
    def register(self, payload: UserRegistration):
        url = self._url(resource=f"/pyrasgo-register", api_version=1)
        response = requests.post(url, json=payload.__dict__)
        status_code = response.status_code
        if status_code == 200:
            return response.json()
        elif status_code == 400:
            raise APIError("Remove the call to pyrasgo.register(...). It is no longer needed")
        elif status_code == 401:
            raise APIError("Invalid Registration. Password must be at least 6 characters")
        else:
            raise APIError("Invalid Registration. Please provide an email and password")

    def _url(self, resource, api_version=None):
        env = Environment.from_environment()
        if '/' == resource[0]:
            resource = resource[1:]
        protocol = 'http' if env.value == 'localhost' else 'https'
        return f"{protocol}://{env.value}/{'' if api_version is None else f'v{api_version}/'}{resource}"