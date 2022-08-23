import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncpg import create_pool
from magic_filter import F

from tgbot.configreader import config
from tgbot.dialogs.misc.setup import setup_dialogs
from tgbot.dialogs.user.user_main import register_handlers_user, schedule_jobs
from tgbot.handlers.group import register_handlers_group
from tgbot.middlewares.db import DbSessionMiddleware

if config.environment == 'PROD':
    logging.basicConfig(filename='bot_webhook.log',
                        filemode='a',
                        level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                        )


async def main():
    logging.warning('Starting bot')
    # Creating DB connections pool
    db_pool = await create_pool(config.postgres_dsn)

    # Creating bot and its dispatcher
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    if config.custom_bot_api:
        bot.session.api = TelegramAPIServer.from_base(config.custom_bot_api, is_local=True)

    # Choosing FSM storage
    if config.bot_fsm_storage == "memory":
        dp = Dispatcher(storage=MemoryStorage())
    else:
        dp = Dispatcher(storage=RedisStorage.from_url(config.redis_dsn,
                                                      key_builder=DefaultKeyBuilder(with_destiny=True)))

    # Allow interaction in private chats (not groups or channels) only
    dp.message.filter(F.chat.type == "private")

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()

    # Register middlewares
    dp.message.middleware(DbSessionMiddleware(db_pool))
    dp.callback_query.middleware(DbSessionMiddleware(db_pool))

    # Routers
    main_router = Router()
    user_router = Router()
    admin_router = Router()
    group_router = Router()

    # Register routers
    dp.include_router(main_router)
    main_router.include_router(user_router)
    main_router.include_router(admin_router)
    main_router.include_router(group_router)
    group_router.message.filter(F.chat.type == "supergroup")

    register_handlers_user(user_router)
    register_handlers_group(group_router)
    setup_dialogs(dp)
    schedule_jobs(dp, scheduler)

    try:

        if not config.webhook_domain:
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        else:
            # Suppress aiohttp access log completely
            aiohttp_logger = logging.getLogger("aiohttp.access")
            aiohttp_logger.setLevel(logging.CRITICAL)

            # Setting webhook
            await bot.set_webhook(
                url=config.webhook_domain + config.webhook_path,
                drop_pending_updates=True,
                allowed_updates=dp.resolve_used_update_types()
            )

            # Creating an aiohttp application
            app = web.Application()
            SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.webhook_path)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host=config.app_host, port=config.app_port)
            await site.start()

            # Running it forever
            await asyncio.Event().wait()

    finally:
        await bot.session.close()


asyncio.run(main())
