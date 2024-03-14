from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.database.models import DBreq, async_session, Subscribe
from sqlalchemy import select, delete


async def get_lastdb(telegram_id: int):
    async with async_session() as session:
        stmt = select(DBreq).where(DBreq.telegram_id == telegram_id).order_by(DBreq.time.desc()).limit(5)
        result = await session.scalars(stmt)
        return result


async def remove_jobs(telegram_id: int, apscheduler: AsyncIOScheduler):
    removed_jobs = []
    async with async_session() as session:
        stmt = select(Subscribe).where(Subscribe.telegram_id == telegram_id)
        result = await session.scalars(stmt)
        for job in result:
            try:
                apscheduler.remove_job(job.job_id)
                removed_jobs.append(job.job_id)
            except JobLookupError as err:
                removed_jobs.append(err)

        await session.execute(delete(Subscribe).where(Subscribe.telegram_id == telegram_id))
        await session.commit()
    return removed_jobs
