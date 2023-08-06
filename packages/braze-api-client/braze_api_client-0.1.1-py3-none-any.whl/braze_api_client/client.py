import requests as rq

from braze_api_client import resources
from braze_api_client.utils import urljoin


class Client:

    def __init__(self, api_key, rest_endpoint):
        
        self._session = rq.Session()
        self._session.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        self._base_endpoint = rest_endpoint

        self._resources = {
            'users': resources.UsersPool(
                urljoin(self._base_endpoint, 'users'), self._session
            )
        }

    @property
    def resources(self):
        return self._resources
    
    @property
    def users(self):
        return self._resources['users']