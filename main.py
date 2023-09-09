import asyncio
import logging
import asyncpg
import contextlib

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.storage.redis import RedisStorage

from core.settings import settings
from core.utils.commands import set_commands
from core.middlewares.dbmiddleware import Dbsession
from core.handlers import basic


async def start_bot(bot: Bot):
    await set_commands(bot)


async def stop_bot(bot: Bot):
    pass


async def create_pool():
    return await asyncpg.create_pool(user=settings.db.user, password=settings.db.password, database=settings.db.database,
                                     host=settings.db.host, port=5432, command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    bot = Bot(settings.bots.bot_token, parse_mode='HTML')
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

    dp.update.middleware.register(Dbsession(pool_connect))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(basic.get_start, Command(commands=['start', 'run']))
    dp.message.register(basic.get_help, Command(commands='help'))

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
