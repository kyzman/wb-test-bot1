from datetime import datetime

from sqlalchemy import BigInteger, func
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from core.settings import settings

DB_URL = f"postgresql+asyncpg://{settings.db.user}:{settings.db.password}@{settings.db.host}/{settings.db.database}"

engine = create_async_engine(DB_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DBreq(Base):
    __tablename__ = 'requests'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    time: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )
    article: Mapped[int] = mapped_column(BigInteger)

    def __repr__(self):
        return f"<User {self.telegram_id}>"


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
