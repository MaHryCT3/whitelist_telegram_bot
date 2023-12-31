from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.messages import START_MESSAGE

start_router = Router()


@start_router.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    await message.answer(START_MESSAGE, disable_web_page_preview=True)
