import asyncio
import logging
import asyncpg
import contextlib

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.storage.redis import RedisStorage

from core.settings import settings, WEBHOOK_PATH, WEBHOOK
from core.utils import services
from core.utils.commands import set_commands
from core.middlewares.dbmiddleware import Dbsession
from core.middlewares.security import CheckAllowedMiddleware
from core.handlers import basic, cards
from core.utils.states import StepsForm


async def start_bot(bot: Bot):
    await set_commands(bot)


async def stop_bot(bot: Bot):
    ...


async def create_pool():
    return await asyncpg.create_pool(user=settings.db.user, password=settings.db.password,
                                     database=settings.db.database,
                                     host=settings.db.host, port=5432, command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    bot = Bot(settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    pool_connect = await create_pool()
    query = f'''
    CREATE TABLE IF NOT EXISTS {settings.db.users_table}
    (
    user_id bigint NOT NULL,
    user_name text COLLATE pg_catalog."default",
    CONSTRAINT {settings.db.users_table}_pkey PRIMARY KEY (user_id)
    );'''
    async with pool_connect.acquire() as connect:
        await connect.execute(query)

    # storage = RedisStorage.from_url('redis://localhost:6379/0')
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.update.middleware.register(CheckAllowedMiddleware())  # проверка доступа к боту, кому разрешено с ним работать.
    dp.update.middleware.register(Dbsession(pool_connect))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(services.cancel_command, Command('cancel'))  # отмена любого действия.
    dp.message.register(basic.get_cards_article, Command(commands=['cardinfo']))
    dp.message.register(cards.get_by_card, StepsForm.search_card)

    dp.message.register(basic.get_start, Command(commands=['start', 'run']))
    dp.message.register(basic.get_help)

    if WEBHOOK:
        app = web.Application()
        webhook_request_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
        webhook_request_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        return app
    else:
        try:
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        except Exception as ex:
            logging.error(f"[!!! Exception] - {ex}", exc_info=True)
        finally:
            await bot.session.close()
            await bot.delete_webhook()


if __name__ == '__main__':
    if WEBHOOK:
        web.run_app(start(), host='0.0.0.0', port=8443)
    else:
        with contextlib.suppress(KeyboardInterrupt, SystemExit):
            asyncio.run(start())
