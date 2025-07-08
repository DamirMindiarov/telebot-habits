from telebot.types import Message

from loader import bot


@bot.message_handler(func=lambda message: message.text == "⚙️Настройки")
async def settings_func(message: Message):
    """Сообщение с настройками"""
    text = "Настройки:"
    text += "\nИзменить количество дней для привития привычки /count_days"
    text += "\nЧто-то еще"
    await bot.send_message(chat_id=message.from_user.id, text=text)