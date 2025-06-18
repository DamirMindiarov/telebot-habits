from telebot.util import quick_markup

buttons = {"login": {"callback_data": "cb_login"}}
keyboard = quick_markup(buttons)
