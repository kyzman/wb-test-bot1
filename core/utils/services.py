import requests
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from core.keyboards.stdkbd import main_kbd
from core.settings import BASE_HELP


async def cancel_command(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(BASE_HELP, parse_mode='HTML', reply_markup=main_kbd)


async def get_wb_card_info(article: int):
    result = requests.get(f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}").json()
    return result.get("data").get("products")[0].get("name")
