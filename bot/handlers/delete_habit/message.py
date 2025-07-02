import requests
from telebot.types import Message

from bot.functions import get_token_by_user_id, if_not_auth
from loader import bot


@bot.message_handler(func=lambda message: "/delete" in message.text)
async def delete_habit(message: Message):
    """Удаляет привычку"""
    habit_id = int(message.text.replace("/delete", ""))

    token = await get_token_by_user_id(user_id=str(message.from_user.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(
        url="http://localhost:8000/habits",
        headers=headers,
        json={"habit_id": str(habit_id)},
    )

    if response.status_code == 401:
        await if_not_auth(bot=bot, user_chat_id=message.from_user.id)

    elif response.status_code == 200 and response.text != "null":
        await bot.send_message(chat_id=message.from_user.id, text="Удалено")
    elif response.status_code == 200:
        await bot.send_message(
            chat_id=message.from_user.id, text="У вас нет привычки с таким id"
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id, text="Что-то пошло не так"
        )
