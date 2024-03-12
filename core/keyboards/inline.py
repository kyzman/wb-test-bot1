from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить информацию по товару', callback_data='select_1')],
    [InlineKeyboardButton(text='Остановить уведомления', callback_data='select_2')],
    [InlineKeyboardButton(text='получить информацию из БД', callback_data='select_2')],
])


def subscribe_kbd(article: int):
    kbd_builder = InlineKeyboardBuilder()
    kbd_builder.button(text='Подписаться', callback_data=f'subscribe_{article}')
    return kbd_builder.as_markup()