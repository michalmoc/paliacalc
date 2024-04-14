from logging import info, warning, debug
from urllib.parse import urljoin

import requests
from joblib import Memory

memory = Memory("cachedir")


@memory.cache
def fetch(url: str, user_agent: str, params=None):
    return requests.get(url, params=params, headers={'User-Agent': user_agent})


class RestApi:
    def __init__(self, api_url, user_agent):
        self.api_url = api_url
        self.user_agent = user_agent

    def get(self, path, params=None):
        url = urljoin(self.api_url, path)
        info(f'fetching "{url}"')
        response = fetch(url, self.user_agent, params=params)
        if response.status_code != 200:
            warning(f'request failed, status {response.status_code}')
            debug(response.headers)
            return {}
        return response.json()
