from aiogram.dispatcher.filters.state import State, StatesGroup


class Register(StatesGroup):
    full_name = State()
    age = State()
    gender = State()
    phone = State()
    occupation = State()
