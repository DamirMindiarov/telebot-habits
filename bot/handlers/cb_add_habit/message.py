import requests
from telebot.types import CallbackQuery, Message

from loader import bot
from bot.states import for_add_habit


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
        text="Введите текст привычки"
    )


@bot.send_message(state=for_add_habit)
async def add_habit_1(message: Message):
    # запрос на добавление привычки
    response = requests.post("http://localhost:8000/habits")
    await bot.send_message(chat_id=message.chat.id, text=response.text)