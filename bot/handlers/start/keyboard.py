from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.util import quick_markup

buttons = {
    "registration": {"callback_data": "cb_registration"},
    "login": {"callback_data": "cb_login"},
}
keyboard = quick_markup(buttons)

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="🎓Регистрация")
button2 = KeyboardButton(text="👔Логин")
button3 = KeyboardButton(text="📋Мои привычки")
button4 = KeyboardButton(text="✔️На сегодня")
main_keyboard.add(button1, button2)
main_keyboard.add(button3, button4)
