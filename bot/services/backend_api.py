from typing import Final

from aiohttp import ClientResponseError

from bot.config import settings
from bot.services.http import HTTPClient


class BackendAPI(HTTPClient):
    BASE_URL = settings.BACKEND_HOST

    PLAYER_EXIST_URL: Final[str] = 'user/exist'
    PLAYER_STEAMID_EXIST_URL: Final[str] = 'user/steamid/exist'
    APPLICATION_CREATE_URL: Final[str] = 'application/'

    async def user_exist(self, telegram_id: int) -> bool:
        try:
            await self.request(self.PLAYER_EXIST_URL, 'GET', query={'telegram_id': telegram_id})
        except ClientResponseError as e:
            if e.status == 404:
                return False
            else:
                raise e
        else:
            return True

    async def steamid_exist(self, steamid: str) -> bool:
        try:
            await self.request(self.PLAYER_STEAMID_EXIST_URL, 'GET', query={'steamid': steamid})
        except ClientResponseError as e:
            if e.status == 404:
                return False
            else:
                raise e
        else:
            return True

    async def application_create(self, telegram_id: int, telegram_username: str, steamid: str) -> None:
        query = {
            'telegram_id': telegram_id,
            'telegram_username': telegram_username,
            'steamid': steamid,
        }

        await self.request(
            self.APPLICATION_CREATE_URL,
            'POST',
            query=query,
        )
