from telebot.util import quick_markup

buttons = {
    "add_habit": {"callback_data": "cb_add_habit"},
}
keyboard = quick_markup(buttons)
