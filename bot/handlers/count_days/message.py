from telebot.types import Message
import requests

from bot.functions import get_token_by_user_id
from loader import bot
from states import HabitState


@bot.message_handler(commands=["count_days"])
async def count_days_func(message: Message):
    """"""
    text = """Для формирования устойчивой привычки в среднем требуется около 66 дней, хотя этот период может варьироваться от 18 до 254 дней в зависимости от сложности действия и индивидуальных особенностей человека. Популярное утверждение о 21 дне не подтверждается научными данными, хотя некоторые исследования показывают, что первые признаки формирования привычки могут появиться через 59-66 дней."""
    text += "\nВыберите кол-во дней от 18 до 254:"
    await bot.send_message(chat_id=message.from_user.id, text=text)
    await bot.set_state(
        user_id=message.from_user.id, state=HabitState.for_count_days
    )


@bot.message_handler(state=HabitState.for_count_days)
async def get_count_days(message: Message):
    """"""
    if not message.text.isdigit() or not 18 <= int(message.text) <= 254:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Нужно ввести целое число от 18 до 254",
        )
    else:
        token = await get_token_by_user_id(user_id=str(message.from_user.id))
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.put(
            "http://localhost:8000/habit/count_days",
            headers=headers,
            json={"days": message.text},
        )

        if response.status_code == 200:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"Вы ввели {message.text} это допустимо",
            )
        else:
            await bot.send_message(
                chat_id=message.from_user.id, text=f"Что-то пошло не так"
            )

        await bot.delete_state(user_id=message.from_user.id)
