import ast
import datetime

import requests
from sqlalchemy import select, delete
from telebot.types import CallbackQuery

from bot.functions import get_token_by_user_id
from loader import bot
from app.database import session_async, HabitsTodayDB, HabitsDB


@bot.callback_query_handler(func=lambda callback: callback.data == "cb_today")
async def show_today_habits(callback: CallbackQuery):
    token = await get_token_by_user_id(user_id=str(callback.from_user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url="http://localhost:8000/habits/today",
                            headers=headers)

    habits_today = ast.literal_eval(response.text.replace("null", "None"))
    sample_habit = """{name}\nВыполнено: /done{id_habit_today}"""
    list_habits = "Список привычек на сегодня:\n"

    for habit_today in habits_today:
        list_habits += sample_habit.format(name=habit_today["name"], id_habit_today=habit_today["id"])
        list_habits += "\n\n"

    await bot.send_message(chat_id=callback.from_user.id, text=list_habits)


