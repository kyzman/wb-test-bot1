import re

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

from core.database.models import async_session, DBreq
from core.utils.services import cancel_command, send_card_msg_info


async def get_by_card(message: types.Message, bot: Bot, state: FSMContext) -> None:
    if message.text == '/cancel':
        await cancel_command(message, state)
        return
    pattern = re.compile(r"^\d+$")
    if len(message.text) > 16 or not pattern.match(message.text):
        await message.answer('Введите корректный номер артикула wildberries!')
        return

    result = await send_card_msg_info(bot, message.chat.id, int(message.text), True)

    if type(result) is not str:
        async with async_session() as session:
            record = DBreq(telegram_id=message.from_user.id, article=int(message.text))
            session.add(record)
            await session.commit()

    await state.clear()

