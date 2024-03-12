from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kbd = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/cardinfo'),
    KeyboardButton(text='/stop'),
    KeyboardButton(text='/getdb')],
], resize_keyboard=True)

cancel_kbd = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/cancel')]], resize_keyboard=True)
