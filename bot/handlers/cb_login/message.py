from telebot.types import CallbackQuery, Message

from loader import bot
from states import PasswordStates
from bot.handlers.cb_login.keyboard import keyboard_forgot_pass, keyboard_show_habits


@bot.callback_query_handler(func=lambda callback: callback.data == "cb_login")
async def login(callback: CallbackQuery):
    await bot.set_state(
        user_id=callback.from_user.id,
        state=PasswordStates.for_login,
    )

    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Введите пароль",
        reply_markup=keyboard_forgot_pass
    )


@bot.message_handler(state=PasswordStates.for_login)
async def login_1(password: Message):
    # если пароль тру
    if password:
        await bot.send_message(
            chat_id=password.chat.id,
            text="Добро пожаловать!",
            reply_markup=keyboard_show_habits
        )
        await bot.delete_state(user_id=password.from_user.id)
    # иначе
    else:
        await bot.send_message(
            chat_id=password.chat.id,
            text="Неверный пароль",
            reply_markup=keyboard_forgot_pass
        )