from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from core.utils.dbconnect import Request
from core.settings import BASE_HELP
from core.keyboards.stdkbd import main_kbd, cancel_kbd
from core.utils.states import StepsForm


async def get_start(msg: types.Message, bot: Bot, request: Request):
    await request.add_data(msg.from_user.id, msg.from_user.first_name)
    await bot.send_message(msg.from_user.id, f"<b>Привет {msg.from_user.first_name}. Рад тебя видеть!</b>")


async def get_help(msg: types.Message, bot: Bot):
    await bot.send_message(msg.from_user.id, BASE_HELP, parse_mode='HTML', reply_markup=main_kbd)


async def get_cards_article(msg: types.Message, bot: Bot, state: FSMContext):
    await bot.send_message(msg.from_user.id, 'Введите артикул товара wildberries:', reply_markup=cancel_kbd)
    await state.set_state(StepsForm.search_card)
