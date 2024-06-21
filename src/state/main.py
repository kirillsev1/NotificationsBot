from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    auth_password = State()

    add_content = State()
    add_perform = State()

    update_content = State()
    update_perform = State()
    delete = State()
