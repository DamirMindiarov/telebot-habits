from telebot.types import CallbackQuery

from loader import bot
from bot.handlers.cb_show_habits.keyboard import keyboard


@bot.callback_query_handler(
    func=lambda callback: callback.data == "cb_show_habits"
)
async def show_habits(callback: CallbackQuery):
    # Запрос к бд на список привычек
    habits = """Список привычек на сегодня:
    Привычка_1
    Выполнена: /done_1
    Не выполнена: /fail_1
    Изменить: /update_1
    Удалить: /delete_1
    
    Привычка_2
    Выполнена: /done_2
    Не выполнена: /fail_2
    Изменить: /update_2
    Удалить: /delete_2
    """
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=habits,
        reply_markup=keyboard,
    )
