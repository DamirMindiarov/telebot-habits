import requests
import json
from telebot.types import CallbackQuery, Message

from bot.functions import get_token_by_user_id, if_not_auth
from loader import bot
from bot.states import HabitState
from bot.handlers.cb_show_habits.keyboard import keyboard
from app.pydentic_models import Habit


@bot.callback_query_handler(
    func=lambda callback: callback.data == "cb_add_habit"
)
async def add_habit(callback: CallbackQuery):
    await bot.set_state(user_id=callback.from_user.id, state=HabitState.for_add_habit)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Введите название новой привычки"
    )


@bot.message_handler(state=HabitState.for_add_habit)
async def add_habit_1(message: Message):
    # запрос на добавление привычки
    token = await get_token_by_user_id(user_id=str(message.from_user.id))

    habit = {"name": message.text, "user_id": str(message.from_user.id)}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post("http://localhost:8000/habits", json=habit, headers=headers)

    if response.status_code == 401:
        await if_not_auth(bot=bot, user_chat_id=message.from_user.id)
        return

    habit_name = json.loads(response.text)["name"]

    await bot.send_message(chat_id=message.chat.id, text=f"Добавлена привычка {habit_name}", reply_markup=keyboard)
    await bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
