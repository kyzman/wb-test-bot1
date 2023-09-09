import asyncio
import logging
import asyncpg

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from core.settings import settings
from core.utils.commands import set_commands
from core.middlewares.dbmiddleware import Dbsession
from core.handlers import basic


async def start_bot(bot: Bot):
    await set_commands(bot)


async def stop_bot(bot: Bot):
    pass


async def create_pool():
    return await asyncpg.create_pool(user='postgres', password='loop', database=settings.bots.db_name,
                                     host='127.0.0.1', port=5432, command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    bot = Bot(settings.bots.bot_token, parse_mode='HTML')
    pool_connect = await create_pool()
    query = f'''
    CREATE TABLE IF NOT EXISTS {settings.bots.db_table_users}
    (
    user_id bigint NOT NULL,
    user_name text COLLATE pg_catalog."default",
    CONSTRAINT {settings.bots.db_table_users}_pkey PRIMARY KEY (user_id)
    );'''
    async with pool_connect.acquire() as connect:
        await connect.execute(query)

    dp = Dispatcher()

    dp.update.middleware.register(Dbsession(pool_connect))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(basic.get_start, Command(commands=['start', 'run']))
    dp.message.register(basic.get_help, Command(commands='help'))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
