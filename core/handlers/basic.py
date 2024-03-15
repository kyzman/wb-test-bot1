from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.settings import BASE_HELP
from core.keyboards.stdkbd import main_kbd, cancel_kbd
from core.utils.services import send_card_msg_info
from core.utils.states import StepsForm
from core.database.requests import get_lastdb, remove_jobs


async def get_help(msg: types.Message, bot: Bot):
    await bot.send_message(msg.from_user.id, BASE_HELP, parse_mode='HTML', reply_markup=main_kbd)


async def get_cards_article(msg: types.Message, bot: Bot, state: FSMContext):
    await bot.send_message(msg.from_user.id, 'Введите артикул товара wildberries:', reply_markup=cancel_kbd)
    await state.set_state(StepsForm.search_card)


async def stop_subscribe(msg: types.Message, bot: Bot, apscheduler: AsyncIOScheduler):
    await remove_jobs(msg.from_user.id, apscheduler)
    await bot.send_message(msg.from_user.id, "Рассылка всех сообщений отменена!", reply_markup=main_kbd)


async def get_db_info(msg: types.Message, bot: Bot):
    result = await get_lastdb(msg.from_user.id)
    output = ""
    for item in result:
        output += f"[{item.id}] : {item.article=} \n"
        await send_card_msg_info(bot, msg.chat.id, item.article, True)
