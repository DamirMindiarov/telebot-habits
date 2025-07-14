import requests

from loader import bot
from telebot.types import CallbackQuery, Message
from states import PasswordStates
from .keyboard import keyboard


@bot.message_handler(func=lambda callback: callback.text == "🎓Регистрация")
@bot.callback_query_handler(
    func=lambda callback: callback.data == "cb_registration"
)
async def create_password(callback: CallbackQuery):
    """В ответ на нажатие кнопки переключает состояние и отправляется сообщение с просьбой ввести пароль"""
    await bot.set_state(
        user_id=callback.from_user.id,
        state=PasswordStates.for_registration,
    )

    await bot.send_message(
        chat_id=callback.from_user.id, text=f"Придумайте пароль(4 символа)"
    )


@bot.message_handler(state=PasswordStates.for_registration)
async def create_password_1(password: Message):
    """При вводе корректного пароль регистрирует пользователя если еще не зарегистрирован"""

    if len(password.text) >= 4:
        data = {"username": password.from_user.id, "password": password.text}
        response = requests.post("http://app:8000/registration", data=data)

        if response.status_code != 201:
            await bot.send_message(
                password.from_user.id,
                text=f"Вы уже зарегистрированы",
                reply_markup=keyboard,
            )
            return
        await bot.send_message(
            password.from_user.id,
            text=f"Вы зарегистрированы",
            reply_markup=keyboard,
        )

    else:
        await bot.send_message(
            chat_id=password.chat.id,
            text="Слишком короткий, надо 4 или более символа",
        )
