import ast
import datetime

import requests
from sqlalchemy import select, delete
from telebot.types import CallbackQuery

from bot.functions import get_token_by_user_id, if_not_auth
from loader import bot
from app.database import session_async, HabitsTodayDB, HabitsDB


@bot.message_handler(func=lambda callback: callback.text == "✔️На сегодня")
@bot.callback_query_handler(func=lambda callback: callback.data == "cb_today")
async def show_today_habits(callback: CallbackQuery):
    """В ответ на нажатие кнопки отправляет пользователю текущий список привычек, которые необходимо выполнить сегодня"""
    token = await get_token_by_user_id(user_id=str(callback.from_user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        url="http://localhost:8000/habits/today", headers=headers
    )

    if response.status_code == 401:
        await if_not_auth(bot=bot, user_chat_id=callback.from_user.id)
        return
    elif response.status_code == 200:
        text = response.text
        text = text.replace("null", "None")
        text = text.replace("true", "True")
        text = text.replace("false", "False")

        habits_today = ast.literal_eval(text)
        sample_habit = """{name}\nВыполнено: /done{id_habit_today}"""
        sample_completed_habit = """{name}\nВыполнено: ✅"""
        list_habits = "Список привычек на сегодня:\n"

        for habit_today in habits_today:
            if habit_today["completed"]:
                list_habits += sample_completed_habit.format(
                    name=habit_today["name"]
                )
            else:
                list_habits += sample_habit.format(
                    name=habit_today["name"],
                    id_habit_today=habit_today["habit_id"],
                )

            list_habits += "\n\n"

        await bot.send_message(chat_id=callback.from_user.id, text=list_habits)
