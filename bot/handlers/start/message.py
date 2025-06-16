from telebot.types import Message

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