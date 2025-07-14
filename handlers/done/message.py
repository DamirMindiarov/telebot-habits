import requests
from telebot.types import Message

from functions import get_token_by_user_id, if_not_auth
from loader import bot


@bot.message_handler(func=lambda message: "/done" in message.text)
async def func_done(message: Message):
    """Регистрирует выполнение привычки"""
    habit_id = int(message.text.replace("/done", ""))

    token = await get_token_by_user_id(user_id=str(message.from_user.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(
        url="http://app:8000/habits/today",
        headers=headers,
        json={"habit_id": str(habit_id)},
    )

    if response.status_code == 401:
        await if_not_auth(bot=bot, user_chat_id=message.from_user.id)
    elif response.status_code == 200 and response.text != "null":
        await bot.send_message(chat_id=message.from_user.id, text="👌👍")
    elif response.status_code == 200:
        await bot.send_message(
            chat_id=message.from_user.id, text="уже выполнена сегодня"
        )
