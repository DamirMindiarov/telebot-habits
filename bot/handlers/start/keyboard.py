from telebot.util import quick_markup

buttons = {
        "registration": {"callback_data": "registration"},
        "login": {"callback_data": "login"},
               }
keyboard = quick_markup(buttons)