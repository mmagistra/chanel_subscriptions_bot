import logging
from aiogram import executor
from create_bot import dp, bot
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import malling

from handlers.handlers_users import register_users_handlers
from handlers.malling import register_malling_handlers

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('bot is online')

register_users_handlers(dp)
register_malling_handlers(dp)


async def on_shutdown(_):
    print('bot is offline')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup, on_shutdown=on_shutdown)
