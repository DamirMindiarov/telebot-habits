import requests
from fastapi import HTTPException, status
from telebot.types import CallbackQuery, Message

from authorization.functions import get_current_user
from loader import bot
from bot.functions import get_token_by_user_id, check_auth
from states import HabitState


@bot.message_handler(func=lambda message: "/update" in message.text)
async def update_habit(message: Message):
    """
    Если пользователь авторизован
    устанавливает состояние для обновления привычки,
    сохраняет id привычки и токен
    """
    user_active_token = await check_auth(user_id=message.from_user.id)

    if user_active_token:
        habit_id = message.text.replace("/update", "")
        await bot.set_state(
            user_id=message.from_user.id,
            state=HabitState.for_update_habit,
        )

        async with bot.retrieve_data(
                message.from_user.id,
                message.chat.id,
        ) as data:
            data['habit_id'] = habit_id
            data["token"] = user_active_token
        text = f"Введите новый текст для привычки с id {habit_id}"

    else:
        text = "Нужно авторизоваться"

    await bot.send_message(
        chat_id=message.from_user.id,
        text=text
    )


@bot.message_handler(state=HabitState.for_update_habit)
async def update_habit_1(message: Message):
    """
    Отправляет запрос на обновление привычки, удаляет состояние.
    """
    async with bot.retrieve_data(
            message.from_user.id,
            message.chat.id,
    ) as data:
        habit_id = data.get('habit_id')
        token = data["token"]

    headers = {"Authorization": f"Bearer {token}"}
    habit = {"habit_id": habit_id, "habit_new_name": message.text}

    response = requests.put(
        url="http://localhost:8000/habits",
        json=habit,
        headers=headers,
    )

    if response.status_code == 200 and response.text != "null":
        text = "Привычка обновлена"
    elif response.status_code == 200:
        text = "У вас не привычки с таким id"
    else:
        text = "Что-то пошло не так"

    await bot.send_message(
        chat_id=message.from_user.id,
        text=text
    )
    await bot.delete_state(user_id=message.from_user.id)
