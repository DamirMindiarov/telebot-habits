from telebot.states import State, StatesGroup


class PasswordStates(StatesGroup):
    for_registration = State()
    for_login = State()
    for_forgot = State()


class HabitState(StatesGroup):
    for_add_habit = State()
    for_update_habit = State()
