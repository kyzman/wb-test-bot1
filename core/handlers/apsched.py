from aiogram import Bot
from core.utils.services import get_wb_card_nested_info


async def send_message_interval(bot: Bot, chat_id: int, article: int):
    await bot.send_message(chat_id, f"Сообщение отправляется с интервалом 5 мин, пока запущен бот - {article}")