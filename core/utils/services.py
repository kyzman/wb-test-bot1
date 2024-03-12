from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from core.keyboards.stdkbd import main_kbd
from core.settings import BASE_HELP


async def cancel_command(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(BASE_HELP, parse_mode='HTML', reply_markup=main_kbd)