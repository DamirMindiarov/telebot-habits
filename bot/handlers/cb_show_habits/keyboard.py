from telebot.util import quick_markup

buttons = {
    "add_habit": {"callback_data": "cb_add_habit"},
    "на сегодня": {"callback_data": "cb_today"},
}
keyboard = quick_markup(buttons)
