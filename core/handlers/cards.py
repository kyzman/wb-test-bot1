import re

from aiogram import types
from aiogram.fsm.context import FSMContext

from core.keyboards.inline import subscribe_kbd
from core.utils.services import cancel_command, get_wb_card_info


async def get_by_card(message: types.Message, state: FSMContext) -> None:
    if message.text == '/cancel':
        await cancel_command(message, state)
        return
    pattern = re.compile(r"^\d+$")
    if len(message.text) > 16 or not pattern.match(message.text):
        await message.answer('Введите корректный номер артикула wildberries!')
        return
    name = await get_wb_card_info(int(message.text))
    name = f'инфа по товару с артикулом {message.text}\n {name}'
    await message.reply(name, reply_markup=subscribe_kbd(int(message.text)))
    await state.clear()
