from environs import Env
from dataclasses import dataclass

BASE_HELP = '''/start - начать работу
/help получить эту помощь
'''


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    channel: int
    bookmarks_chat: int

@dataclass
class Db:
    host: str
    database: str
    user: str
    password: str
    users_table: str


@dataclass
class Settings:
    bots: Bots
    db: Db


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            channel=env.int("MY_CHANNEL"),
            bookmarks_chat=env.int("MY_CHAT_BOOKMARKS")
        ),
        db=Db(
            host=env.str("DB_HOST"),
            database=env.str("DB_DATABASE"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            users_table=env.str("DB_TABLE_USERS"),

        )
    )


settings = get_settings('input')

# file 'input' must be in root folder and have text format such as:
# TOKEN=your bot token
# ADMIN_ID=your telegram ID
# MY_CHANNEL=
# MY_CHAT_BOOKMARKS=

# DB_HOST=your DataBase host name
# DB_DATABASE=your database name
# DB_USER=your DataBase access user
# DB_PASSWORD=your DataBase access password
# DB_TABLE_USERS=your table for store user IDs in DataBase
