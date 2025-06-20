import requests
from telebot.types import CallbackQuery, Message

from bot.functions import get_token_by_user_id
from loader import bot
from bot.states import for_add_habit
from bot.handlers.cb_show_habits.keyboard import keyboard
from app.pydentic_models import Habit


@bot.callback_query_handler(
    func=lambda callback: callback.data == "cb_add_habit"
)
async def add_habit(callback: CallbackQuery):
    await bot.set_state(user_id=callback.from_user.id, state=for_add_habit)
    # habits = """Список привычек на сегодня:
    # Привычка_1
    # Выполнена: [<dddd>](</done_1>)
    # Не выполнена: /fail_1
    # Изменить: /update_1
    # Удалить: /delete_1
    #
    # Привычка_2
    # Выполнена: /done_2
    # Не выполнена: /fail_2
    # Изменить: /update_2
    # Удалить: /delete_2
    # """
    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Введите название новой привычки"
    )


@bot.message_handler(state=for_add_habit)
async def add_habit_1(message: Message):
    # запрос на добавление привычки
    token = await get_token_by_user_id(user_id=str(message.from_user.id))

    habit = {"name": message.text, "user_id": str(message.from_user.id)}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post("http://localhost:8000/habits", json=habit, headers=headers)
    # print(response)
    await bot.send_message(chat_id=message.chat.id, text="await", reply_markup=keyboard)