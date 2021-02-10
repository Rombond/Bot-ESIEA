import aiohttp
import requests

BASEURL = 'https://learning.esiea.fr/'
SERVICE = 'webservice/'
API = 'rest/'
CONNECTION = 'server.php?'
FORMAT = 'moodlewsrestformat=json'
TOKEN = '&wstoken='

REQUEST = f'{BASEURL}{SERVICE}{API}{CONNECTION}{FORMAT}{TOKEN}'


class Request:

    def __init__(self, token):
        self.token = token
        self.request = requests

    async def get(self, function, **kwargs):
        url = REQUEST + self.token
        url += f'&wsfunction={function}'

        for key, value in kwargs.items():
            url += f'&{key}={value}'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    if r.status == 200:
                        js = await r.json()
                        return js

        except requests.exceptions.HTTPError as httperror:
            return f'HTTP error occured: {httperror}'

        except Exception as err:
            return f'Other error occured: {err}'

    def post(self, *args, **kwargs):
        pass
