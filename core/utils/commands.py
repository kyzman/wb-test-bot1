from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='cardinfo',
            description='Получить информацию по товару'
        ),
        BotCommand(
            command='stop',
            description='Остановить уведомления'
        ),
        BotCommand(
            command='getdb',
            description='получить информацию из БД'
        ),

    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
