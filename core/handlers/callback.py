from aiogram.types import CallbackQuery


async def subscribe(call: CallbackQuery):  # TODO
    await call.answer(f"[Ещё не реализовано!] Вы подписались на товар с артикулом {call.data}")