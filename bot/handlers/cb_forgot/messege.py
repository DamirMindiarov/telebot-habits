from telebot.types import CallbackQuery, Message

from authorization.functions import update_password
from loader import bot
from states import PasswordStates


@bot.callback_query_handler(func=lambda callback: callback.data == "cb_forgot")
async def cb_forgot(callback: CallbackQuery):
    await bot.set_state(user_id=callback.from_user.id,
                        state=PasswordStates.for_forgot)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Введите новый пароль(4 символа минимум)"
    )


@bot.message_handler(state=PasswordStates.for_forgot)
async def cb_forgot_1(password: Message):
    if len(password.text) >= 4:
        await update_password(user_id=str(password.from_user.id),
                              password=password.text)
        await bot.send_message(
            chat_id=password.chat.id,
            text="Пароль обновлен"
        )
        await bot.delete_state(user_id=password.from_user.id)
    else:
        await bot.send_message(
            chat_id=password.chat.id,
            text="Слишком короткий, надо 4 или более символа"
        )
