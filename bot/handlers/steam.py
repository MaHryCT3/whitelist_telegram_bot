from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiohttp import ClientResponseError

from bot.messages import (
    APPLICATION_HAVE_SEND,
    INVALID_STEAM_LINK,
    NOT_PUT_STEAM_LINK,
    STEAMID_ALREADY_IN_USE,
    YOU_ALREADY_SEND_APPLICATION,
    STEAM_SERVICE_IS_UNAVAILABLE
)
from bot.services.backend_api import BackendAPI
from bot.services.steam_link_validator import SteamLinkValidator

steam_router = Router()


@steam_router.message(
    F.text.startswith('765611')
    | F.text.contains(SteamLinkValidator.STEAM_LINK_WITH_STEAMID)
    | F.text.contains(SteamLinkValidator.STEAM_LINK_WITH_VANITY_URL)
    | F.text.contains('steamcommunity')
)
async def command_steam_handler(message: Message):
    steam_link = message.text
    if not steam_link:
        return await message.answer(NOT_PUT_STEAM_LINK)

    backend_api = BackendAPI()
    if await backend_api.user_exist(message.from_user.id):
        return await message.answer(YOU_ALREADY_SEND_APPLICATION)

    steam_link_validator = SteamLinkValidator()
    try:
        steamid = await steam_link_validator.validate_steamid(steam_link)
    except ClientResponseError as e:
        return await message.answer(STEAM_SERVICE_IS_UNAVAILABLE)
    except Exception:
        return await message.answer(STEAM_SERVICE_IS_UNAVAILABLE)

    if steamid is None:
        return await message.answer(INVALID_STEAM_LINK)

    if await backend_api.steamid_exist(steamid):
        return await message.answer(STEAMID_ALREADY_IN_USE)

    await backend_api.application_create(message.from_user.id, message.from_user.username or 'ПРОФИЛЬ_СКРЫТ', steamid)
    await message.answer(APPLICATION_HAVE_SEND, disable_web_page_preview=True, reply_markup=get_subscribe_inline())


def get_subscribe_inline():
    builder = InlineKeyboardBuilder()
    subscribe_button = InlineKeyboardButton(text='Подписаться на ONE LIFE', url='https://t.me/oneliferust')
    builder.add(subscribe_button)
    return builder.as_markup()


