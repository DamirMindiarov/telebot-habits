from telebot.util import quick_markup

buttons_forgot_pass = {"forgot": {"callback_data": "cb_forgot"}}
keyboard_forgot_pass = quick_markup(buttons_forgot_pass)

buttons_show_habits = {"show_habits": {"callback_data": "cb_show_habits"}}
keyboard_show_habits = quick_markup(buttons_show_habits)
