from logging import info
from typing import Any

from remote.rest_api import RestApi

PALIA_API_URL = 'https://api.paliapedia.com'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'


class PaliaApi(RestApi):
    def __init__(self):
        super().__init__(PALIA_API_URL, USER_AGENT)
        self.version = self.get_version()

    def get_version(self):
        return self.get('api/version')['version']

    def palia_get(self, path):
        return self.get(f'{path}/api/{self.version}')

    def get_list(self, path, params) -> [Any]:
        response = self.get(f'{path}/page/1/api/{self.version}', params=params)
        response = response['pagedData']
        page_count = response['pageCount']
        results = list(response['data'])
        for i in range(2, page_count + 1):
            info("getting more pages")
            response = self.get(f'{path}/page/{i}/api/{self.version}', params=params)
            results += response['pagedData']['data']
        return results

    def get_item(self, key: str):
        return self.palia_get(f'item/{key}')

    def get_recipe(self, key: str):
        return self.palia_get(f'recipe/{key}')

    def get_tag(self, key: str):
        return self.get_list(f'items', params={'filters': 'tag:' + key})
