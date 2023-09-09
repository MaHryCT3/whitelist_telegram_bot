from typing import Final

from bot.config import settings
from bot.services.http import HTTPClient


class SteamAPI(HTTPClient):
    BASE_URL = 'http://api.steampowered.com/'

    API_KEY: Final[str] = settings.STEAM_KEY

    GET_PLAYER_INFO_URL: Final[str] = 'ISteamUser/GetPlayerSummaries/v0002'
    RESOLVE_STEAM_VANITY_URL: Final[str] = 'ISteamUser/ResolveVanityURL/v1/'

    async def is_profile_exist(self, steamid: str) -> bool:
        response = await self.request(
            url=self.GET_PLAYER_INFO_URL,
            http_method='GET',
            query=self._get_query(steamids=steamid),
        )
        response_json = await response.json()

        try:
            players = list(response_json['response']['players'])
        except (AttributeError, KeyError):
            players = []

        return bool(players)

    async def resolve_steam_url(self, vanity_url: str) -> str | None:
        response = await self.request(
            url=self.RESOLVE_STEAM_VANITY_URL,
            http_method='GET',
            query=self._get_query(vanityurl=vanity_url),
        )
        response_json = await response.json()

        try:
            steamid = response_json['response']['steamid']
        except (AttributeError, KeyError):
            return

        return steamid

    def _get_query(self, **kwargs) -> dict:
        return {'key': self.API_KEY, **kwargs}
