from aiogram import executor, types
from loguru import logger
from loader import dp
from utils.notify_admins import on_startup_notify

import handlers


async def on_startup(dp):
    await on_startup_notify(dp)
    logger.info("Бот запущен")


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup,
                           skip_updates=True,
                           allowed_updates=types.AllowedUpdates.all())
