import aiohttp
from requests import post


class Token:

    def __str__(self):
        return 'Token request object'

    async def post(self, username=None, password=None):
        username = f'&username={username}'
        password = f'&password={password}'

        url = f'https://learning.esiea.fr/login/token.php?service=moodle_mobile_app{username}{password}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    data = await r.json()

        return data['token']
