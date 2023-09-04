from aiogram import Bot, types
from core.utils.dbconnect import Request
from core.settings import BASE_HELP


async def get_start(msg: types.Message, bot: Bot, request: Request):
    await request.add_data(msg.from_user.id, msg.from_user.first_name)
    await bot.send_message(msg.from_user.id, f"<b>Привет {msg.from_user.first_name}. Рад тебя видеть!</b>")


async def get_help(msg: types.Message, bot: Bot):
    await bot.send_message(msg.from_user.id, BASE_HELP, parse_mode='HTML')
