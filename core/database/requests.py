from core.database.models import DBreq, async_session
from sqlalchemy import select


async def get_lastdb(telegram_id: int):
    async with async_session() as session:
        stmt = select(DBreq).where(DBreq.telegram_id == telegram_id).order_by(DBreq.time.desc()).limit(5)
        result = await session.scalars(stmt)
        return result
