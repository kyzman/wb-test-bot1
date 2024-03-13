import re

from aiogram import types
from aiogram.fsm.context import FSMContext

from core.database.models import async_session, DBreq
from core.keyboards.inline import subscribe_kbd
from core.utils.services import cancel_command, get_wb_card_nested_info


async def get_by_card(message: types.Message, state: FSMContext) -> None:
    if message.text == '/cancel':
        await cancel_command(message, state)
        return
    pattern = re.compile(r"^\d+$")
    if len(message.text) > 16 or not pattern.match(message.text):
        await message.answer('Введите корректный номер артикула wildberries!')
        return
    data = await get_wb_card_nested_info(
        int(message.text))  # это конечно плохо, что функция возвращает разные типы данных, но в данном конкретном случае почему бы и нет?

    if type(data) is str:
        output = data
        kbd = None
    else:
        output = data.get("products")
        kbd = subscribe_kbd(int(message.text))

    async with async_session() as session:
        record = DBreq(telegram_id=message.from_user.id, article=int(message.text))
        session.add(record)
        await session.commit()

    name = f'инфа по товару с артикулом {message.text}\n {output}'
    await message.reply(name, reply_markup=kbd)
    await state.clear()

