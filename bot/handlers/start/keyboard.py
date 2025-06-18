from telebot.util import quick_markup

buttons = {
        "registration": {"callback_data": "cb_registration"},
        "login": {"callback_data": "cb_login"},
               }
keyboard = quick_markup(buttons)