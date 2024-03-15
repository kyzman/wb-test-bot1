import asyncio
import logging
import contextlib

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler_di import ContextSchedulerDecorator

from core.database.models import async_main
from core.handlers.callback import subscribe
from core.middlewares.apschedulemiddleware import SchedulerMiddleware
# from aiogram.fsm.storage.redis import RedisStorage

from core.settings import settings, WEBHOOK_PATH, WEBHOOK
from core.utils import services
from core.utils.commands import set_commands
from core.middlewares.security import CheckAllowedMiddleware
from core.handlers import basic, cards
from core.utils.states import StepsForm

from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def start_bot(bot: Bot):
    await set_commands(bot)
    await async_main()


async def stop_bot(bot: Bot):
    ...


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    bot = Bot(settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # storage = RedisStorage.from_url('redis://localhost:6379/0')
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Asia/Yekaterinburg"))
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.start()

    dp.update.middleware.register(CheckAllowedMiddleware())  # проверка доступа к боту, кому разрешено с ним работать.
    dp.update.middleware.register(SchedulerMiddleware(scheduler))  # регистрация, чтобы можно было передавать объект в функции

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(services.cancel_command, Command('cancel'))  # отмена любого действия, кроме уведомлений.
    dp.message.register(basic.get_cards_article, Command(commands=['cardinfo']))
    dp.message.register(basic.stop_subscribe, Command(commands=['stop']))
    dp.message.register(basic.get_db_info, Command(commands=['getdb']))
    dp.message.register(cards.get_by_card, StepsForm.search_card)

    dp.callback_query.register(subscribe, F.data.startswith('subscribe_'))

    dp.message.register(basic.get_help)

    if WEBHOOK:
        app = web.Application()
        webhook_request_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
        webhook_request_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        return app
    else:
        try:
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), polling_timeout=30)
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
