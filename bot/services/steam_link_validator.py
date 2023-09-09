from typing import Final

from bot.services.steam_api import SteamAPI


class SteamLinkValidator:
    STEAM_LINK_WITH_STEAMID: Final[str] = 'steamcommunity.com/profiles/'
    STEAM_LINK_WITH_VANITY_URL: Final[str] = 'steamcommunity.com/id/'
    STEAMID_SIGN: Final[str] = '765611'

    def __init__(self):
        self.steam_api = SteamAPI()

    async def validate_steamid(self, link: str) -> str | None:
        steamid = None
        steamid_validated = False

        if self.is_steamid(link):
            steamid = link
        elif self.is_steam_link_with_steamid(link):
            steamid = self.get_steamid_from_link(link)
        elif self.is_steam_link_with_vanity_url(link):
            custom_steamid = self.get_steamid_from_link(link)
            steamid = await self.steam_api.resolve_steam_url(custom_steamid)
            steamid_validated = True

        if steamid is None:
            return None

        if not steamid_validated:
            steamid_validated = await self.steam_api.is_profile_exist(steamid)

        if steamid_validated:
            return steamid

    def is_steam_link_with_steamid(self, link: str) -> bool:
        return self.STEAM_LINK_WITH_STEAMID in link

    def is_steam_link_with_vanity_url(self, link: str) -> bool:
        return self.STEAM_LINK_WITH_VANITY_URL in link

    def is_steamid(self, link: str) -> bool:
        return link.startswith(self.STEAMID_SIGN)

    @staticmethod
    def get_steamid_from_link(steam_link: str) -> str:
        steam_link = steam_link.removesuffix('/')
        paths = steam_link.split('/')
        return paths[-1]
