import logging
from aiogram import executor
from create_bot import dp


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('bot is online')


async def on_shutdown(_):
    print('bot is offline')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
