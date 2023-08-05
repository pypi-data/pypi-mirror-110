import asyncio

from aiohttp import ClientResponse, ClientSession

from .errors import (
    AuthenticationFailed,
    FlylineBadRequest,
    FlylineItemNotFound,
    FlylineServerError,
)


class FlylineBaseClient:
    BASE_URL = "https://api.flyline.io/api"

    def __init__(self, key: str):
        self._key = key
        headers = {"Authorization": f"FToken {self._key}"}
        self._loop = asyncio.get_event_loop()
        self.session = ClientSession(headers=headers, loop=self._loop)

    @classmethod
    async def parse_response(cls, response: ClientResponse):
        if response.status == 401:
            raise AuthenticationFailed()
        elif response.status == 404:
            raise FlylineItemNotFound()
        elif response.status == 500:
            raise FlylineServerError()

        res = await response.json()
        if response.status == 400:
            raise FlylineBadRequest(res)
        else:
            return res

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
