from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from core.settings import BASE_HELP
from core.keyboards.stdkbd import main_kbd, cancel_kbd
from core.utils.states import StepsForm
from core.database.requests import get_lastdb


async def get_help(msg: types.Message, bot: Bot):
    await bot.send_message(msg.from_user.id, BASE_HELP, parse_mode='HTML', reply_markup=main_kbd)


async def get_cards_article(msg: types.Message, bot: Bot, state: FSMContext):
    await bot.send_message(msg.from_user.id, 'Введите артикул товара wildberries:', reply_markup=cancel_kbd)
    await state.set_state(StepsForm.search_card)


async def stop_subscribe(msg: types.Message, bot: Bot):  # TODO

    await bot.send_message(msg.from_user.id, "[Ещё не реализовано!] Рассылка всех сообщений отменена!", reply_markup=main_kbd)


async def get_db_info(msg: types.Message, bot: Bot):
    result = await get_lastdb(msg.from_user.id)
    output = ""
    for item in result:
        output += f"[{item.id}] : {item.article=} "
    await bot.send_message(msg.from_user.id, f"Ваши последние 5 запросов: {output}", reply_markup=main_kbd)
