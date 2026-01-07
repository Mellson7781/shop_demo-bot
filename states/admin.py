from aiogram.fsm.state import State, StatesGroup


class AddAdmin(StatesGroup):
    username = State()


class DelAdmin(StatesGroup):
    username = State()