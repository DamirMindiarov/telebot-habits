import requests
from telebot.types import Message, CallbackQuery

from bot.handlers.cb_notifications.keyboard import keyboard
from bot.functions import get_token_by_user_id
from loader import bot


@bot.message_handler(func=lambda callback: callback.text == "🔔Уведомления")
async def cb_notifications(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Отключить/включить",
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda callback: callback.data == "cb_notifications")
async def cb_notifications_off(callback: CallbackQuery):
    token = await get_token_by_user_id(user_id=str(callback.from_user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.put(
        url="http://localhost:8000/habits/notifications", headers=headers
    )

    if response.status_code == 200:
        await bot.send_message(chat_id=callback.from_user.id, text=response.text)
    else:
        await bot.send_message(chat_id=callback.from_user.id,
                               text="Вы не авторизованы")