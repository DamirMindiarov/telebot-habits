import requests
from sqlalchemy import select
from telebot.types import CallbackQuery

from app.database import session_async, HabitsDB, UsersDB
from bot.functions import get_token_by_user_id
from loader import bot
from bot.handlers.cb_show_habits.keyboard import keyboard


@bot.callback_query_handler(
    func=lambda callback: callback.data == "cb_show_habits"
)
async def show_habits(callback: CallbackQuery):
    # Запрос к бд на список привычек
    # async with session_async() as session:
    #     habits = await session.execute(select(HabitsDB).where(UsersDB.id == callback.from_user.id))
    token = await get_token_by_user_id(user_id=str(callback.from_user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url="http://localhost:8000/habits", headers=headers)
    # habits = """Список привычек на сегодня:
    # Привычка_1
    # Выполнена: 0 из 21
    # Не выполнена: 0 из 21
    # Изменить: /update_1
    # Удалить: /delete_1
    #
    # Привычка_2
    # Выполнена: 0 из 21
    # Не выполнена: 0 из 21
    # Изменить: /update_2
    # Удалить: /delete_2
    # """
    habits = response.text
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=habits,
        reply_markup=keyboard,
    )
