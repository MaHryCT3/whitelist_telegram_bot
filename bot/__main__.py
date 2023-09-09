import asyncio

from aiogram import Bot, Dispatcher

from bot.config import settings
from bot.handlers import routers

dp = Dispatcher()
dp.include_routers(*routers)

bot = Bot(token=settings.TELEGRAM_TOKEN)

asyncio.run(dp.start_polling(bot))
