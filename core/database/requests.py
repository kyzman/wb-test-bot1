from core.database.models import DBreq, async_session
from sqlalchemy import select


async def get_lastdb():
    async with async_session() as session:
        result = await session.scalar(select(DBreq))
        return result
