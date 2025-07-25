import requests
from telebot.types import Message

from functions import get_token_by_user_id
from loader import bot
from states import HabitState


@bot.message_handler(func=lambda message: "/update" in message.text)
async def update_habit(message: Message):
    """
    устанавливает состояние для обновления привычки,
    сохраняет id привычки и токен
    """

    habit_id = message.text.replace("/update", "")
    await bot.set_state(
        user_id=message.from_user.id,
        state=HabitState.for_update_habit,
    )

    async with bot.retrieve_data(
        message.from_user.id,
        message.chat.id,
    ) as data:
        data["habit_id"] = habit_id
    text = f"Введите новый текст для привычки с id {habit_id}"

    await bot.send_message(chat_id=message.from_user.id, text=text)


@bot.message_handler(state=HabitState.for_update_habit)
async def update_habit_1(message: Message):
    """
    Отправляет запрос на обновление привычки, удаляет состояние.
    """

    async with bot.retrieve_data(
        message.from_user.id,
        message.chat.id,
    ) as data:
        habit_id = data.get("habit_id")

    token = await get_token_by_user_id(user_id=str(message.from_user.id))
    headers = {"Authorization": f"Bearer {token}"}
    habit = {"habit_id": habit_id, "habit_new_name": message.text}

    response = requests.put(
        url="http://app:8000/habits",
        json=habit,
        headers=headers,
    )

    if response.status_code == 200 and response.text != "null":
        text = "Привычка обновлена"
    elif response.status_code == 200:
        text = "У вас не привычки с таким id"
    else:
        text = "Что-то пошло не так"

    await bot.send_message(chat_id=message.from_user.id, text=text)
    await bot.delete_state(user_id=message.from_user.id)
