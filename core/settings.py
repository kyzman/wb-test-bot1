from environs import Env
from dataclasses import dataclass

BASE_HELP = '''/start - начать работу
/help получить эту помощь
'''


@dataclass
class Bots:
    bot_token: str
    admin_id: str
    db_name: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            db_name=env.str("DB_NAME"),
        )
    )


settings = get_settings('input')

# file 'input' must be in root folder and have text format such as:
# TOKEN=your bot token
# ADMIN_ID=your telegram ID
# DB_NAME=your database name
