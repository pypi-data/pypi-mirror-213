from .qb_errors import *
import requests
import time

class QuickbaseClient:
    def __init__(self, credentials, timeout=90, database=None):
        self.username = credentials.get('username')
        self.password = credentials.get('password')
        self.realmhost = credentials.get('realmhost')
        self.base_url = credentials.get('base_url')
        self.user_token = credentials.get('user_token')
        self.timeout = timeout
        self.database = database

        if not self.base_url:
            raise QBAuthError('missing base_url')
        if not self.realmhost:
            self.realmhost = self.base_url.split('https://')[1]

    def _make_request(self, url, action, headers, data, params, json=False):
        kwargs = {
            'headers': headers,
            'timeout': self.timeout,
        }
        if data and headers.get('Content-Type') == 'application/json':
            kwargs['json'] = data
        elif data:
            kwargs['data'] = data
        if params:
            kwargs['params'] = params


        if action.lower() == 'get':
            response: requests.models.Response = requests.get(url, **kwargs)
        elif action.lower() == 'post':
            response: requests.models.Response = requests.post(url, **kwargs)
        elif action.lower() == 'delete':
            response: requests.models.Response = requests.delete(url, **kwargs)
        else:
            raise ValueError('invalid action')
        
        if response.status_code == 401 or response.status_code == 403:
            raise QBAuthError('Invalid credentials')
        elif response.status_code == 404:
            raise QBConnectionError('Connection Error: Invalid URL')
        elif response.status_code == 400:
            raise QuickbaseError('Response Error: Invalid request', response)
        elif response.status_code == 429:
            raise QBResponseError('Response Error: Too many requests', response)
        elif response.status_code == 500:
            raise QBResponseError('Response Error: Internal Quickbase Server Error', response)
        elif response.status_code == 504:
            raise QBResponseError('Response Error: Gateway Timeout', response)
        if json:
            try:
                return response.json()
            except Exception as e:
                raise QuickbaseError('Response Error: Invalid JSON or no data given', response) from e
        else:
            return response
        
    def _request(self, url, action, headers, data=None, params=None, json=False):
        tries = 0

        while tries < 10:
            try:
                return self._make_request(url, action, headers, params=params, data=data, json=json)
            except requests.exceptions.Timeout as e:
                tries += 1
                time.sleep(1)
                pass
            except QBResponseError as e:
                if e.response.status_code == 429:
                    tries += 1
                    time.sleep(5)
                    pass
                if e.response.status_code == 504:
                    tries += 1
                    time.sleep(30)
                    pass
                else:
                    raise e from e
        raise QBConnectionError('Connection Error: Timeout')