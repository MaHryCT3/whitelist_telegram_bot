import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.config import settings
from bot.handlers import routers

dp = Dispatcher()
dp.include_routers(*routers)

bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)

asyncio.run(dp.start_polling(bot))
