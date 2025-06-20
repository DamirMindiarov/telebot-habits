from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from loader import bot
from bot.handlers.start.keyboard import keyboard


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message: Message):
    text = 'Привет, нужно зарегистрироваться/войти'

    await bot.send_message(
        chat_id=message.from_user.id,
        text=text,
        reply_markup=keyboard
    )
    key = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="Регистрация")
    button2 = KeyboardButton(text="Логин")
    button3 = KeyboardButton(text="Мои привычки")
    key.add(button1)
    key.add(button2, button3)

    await bot.send_message(
        chat_id=message.from_user.id,
        text="Так же есть удобная навигация на клавиатуре",
        reply_markup=key
    )