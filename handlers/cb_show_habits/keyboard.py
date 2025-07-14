from telebot.util import quick_markup

buttons = {
    "добавить": {"callback_data": "cb_add_habit"},
    "на сегодня": {"callback_data": "cb_today"},
}
keyboard = quick_markup(buttons)
