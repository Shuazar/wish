import asyncio
import logging
import os
import django

from tgbot.handlers.echo import echo_router

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "django_project.wish.wish.settings"
)
os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config

from tgbot.middlewares.config import ConfigMiddleware
from tgbot.services import broadcaster
from tgbot.handlers.admin import admin_router
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admin_ids: list[int], config):
    logging.info("Creating Django...")
    await broadcaster.broadcast(bot, admin_ids, "Bot is working")


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    for router in [
        admin_router,
        echo_router
    ]:
        dp.include_router(router)
        # dp.include_router(questions.router)
        # dp.include_router(different_types.router)

    register_global_middlewares(dp, config)
    logging.info(f"Create connection to database")

    await on_startup(bot, config.tg_bot.admin_ids, config)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot is started!")
