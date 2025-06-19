from telebot.states import State, StatesGroup


class PasswordStates(StatesGroup):
    for_registration = State()
    for_login = State()
    for_forgot = State()


for_add_habit = State()