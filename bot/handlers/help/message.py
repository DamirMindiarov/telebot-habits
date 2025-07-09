from telebot.types import Message

from loader import bot
from bot.handlers.start.keyboard import main_keyboard


@bot.message_handler(commands=["help"])
async def command_help(message: Message):
    text = "🌻\n🔹Навигация происходит по клавиатуре⌨️"

    text += """\n🔹Для использования бота необходимо зарегистрироваться(кнопка "Регистрация")."""
    text += """\n🔹Далее необходимо войти - кнопка "Логин"."""
    text += """\n🔹Чтобы увидеть список всех ваших привычек и их прогресс -> "Мои привычки"."""
    text += """\n🔹Чтобы добавить привычку - нажмите "Мои привычки" -> "Добавить"."""
    text += """\n🔹Чтобы посмотреть привычки, которые нужно выполнить сегодня - "На сегодня"."""
    text += """\n🔹Чтобы отметить привычку как выполненную - в списке "На сегодня" нажмите "done"""
    text += """\n🔹Отключить уведомления - "Уведомления" -> "отключить"""

    await bot.send_message(
        chat_id=message.from_user.id, text=text, reply_markup=main_keyboard
    )
