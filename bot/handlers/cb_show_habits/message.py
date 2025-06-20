import ast

import requests
from telebot.types import CallbackQuery

from bot.functions import get_token_by_user_id
from bot.handlers.cb_show_habits.keyboard import keyboard
from loader import bot


@bot.callback_query_handler(
    func=lambda callback: callback.data == "cb_show_habits"
)
async def show_habits(callback: CallbackQuery):
    token = await get_token_by_user_id(user_id=str(callback.from_user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url="http://localhost:8000/habits",
                            headers=headers)
    habits = ast.literal_eval(response.text)

    sample_habit = """{name}\nВыполнена: {count_done} из 21\nИзменить: /update{id_habit}\nУдалить: /delete{id_habit}"""
    list_habits = "Список привычек:\n"

    for habit in habits:
        list_habits += sample_habit.format(name=habit["name"],
                                           count_done=habit["count_done"],
                                           id_habit=habit["id"])
        list_habits += "\n\n"

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=list_habits,
        reply_markup=keyboard,
    )
