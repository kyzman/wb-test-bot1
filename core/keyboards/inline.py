from aiogram.utils.keyboard import InlineKeyboardBuilder


def subscribe_kbd(article: int):
    kbd_builder = InlineKeyboardBuilder()
    kbd_builder.button(text='Подписаться', callback_data=f'subscribe_{article}')
    return kbd_builder.as_markup()