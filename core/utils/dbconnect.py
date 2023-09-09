import asyncpg
from core.settings import settings


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, user_name):
        query = f"INSERT INTO {settings.bots.db_table_users} (user_id, user_name) VALUES ({user_id}, '{user_name}')" \
                f" ON CONFLICT (user_id) DO UPDATE SET user_name = '{user_name}';"
        await self.connector.execute(query)