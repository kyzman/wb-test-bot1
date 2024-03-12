from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    search_card = State()