from datetime import datetime

from sqlalchemy import BigInteger, func, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from core.settings import DB_URL

engine = create_async_engine(DB_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass
    id: Mapped[int] = mapped_column(primary_key=True)


class DBreq(Base):
    __tablename__ = 'requests'

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    time: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )
    article: Mapped[int] = mapped_column(BigInteger, nullable=False)

    task_id: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"<User {self.telegram_id}>"


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
