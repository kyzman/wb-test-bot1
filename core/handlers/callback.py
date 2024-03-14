from aiogram import Bot
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.database.models import async_session, Subscribe
from core.utils.services import send_card_msg_info


async def subscribe(call: CallbackQuery, apscheduler: AsyncIOScheduler):
    article = int(call.data[10:])
    job = apscheduler.add_job(send_card_msg_info, trigger='interval', seconds=300,
                        kwargs={'chat_id': call.message.chat.id, 'article': article,
                                'add_subscribe_kbd': False, 'header': '*** ОПОВЕЩЕНИЕ ***'})
    async with async_session() as session:
        record = Subscribe(telegram_id=call.from_user.id, article=article, job_id=job.id)
        session.add(record)
        await session.commit()

    await call.answer(f"Вы подписались на товар с артикулом {article}\n Ожидайте уведомлений!")
