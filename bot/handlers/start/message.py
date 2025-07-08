from telebot.types import Message

from loader import bot
from .keyboard import keyboard, main_keyboard


@bot.message_handler(commands=["start"])
async def send_welcome(message: Message):
    """Отправляет приветственное сообщение"""
    text = "нужно зарегистрироваться/войти"

    await bot.send_message(
        chat_id=message.from_user.id, text="Привет", reply_markup=main_keyboard
    )

    await bot.send_message(
        chat_id=message.from_user.id, text=text, reply_markup=keyboard
    )
