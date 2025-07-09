import asyncio
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.async_telebot import AsyncTeleBot

from app.database import HabitsDB, HabitsTodayDB, UsersDB
from app.database import session_async
from bot.loader import bot

scheduler = AsyncIOScheduler()


async def get_users_id(session: AsyncSession) -> list[str]:
    """Возвращает список user_id кому нужно отправить уведомление"""
    date = datetime.datetime.now().date()

    # 1) в таблице HabitsDB есть хотя-бы одна привычка с count_done < days_to_form
    ui_not_count_done = await session.execute(
        select(HabitsDB.user_id).where(
            HabitsDB.count_done < HabitsDB.days_to_form
        )
    )

    # 1.1) если у пользователя в таблице HabitsTodayDB есть привычка с сегодняшней датой и с complete == None
    ui_not_complete = await session.execute(
        select(HabitsTodayDB.user_id).where(
            HabitsTodayDB.date == date,
            HabitsTodayDB.completed == None,
        )
    )

    # 1.2) если у пользователя в таблице HabitsTodayDB отсутствует привычка с сегодняшней датой
    ui_not_date = await session.execute(
        select(HabitsDB.user_id, HabitsTodayDB)
        .join(
            HabitsTodayDB, HabitsDB.id == HabitsTodayDB.habit_id, isouter=True
        )
        .where(HabitsTodayDB.date == None)
    )

    # 2) если у пользователя включены уведомления
    ui_with_notifications_on = await session.execute(
        select(UsersDB.user_id).where(UsersDB.notifications == "+")
    )

    ui_not_count_done = list(ui_not_count_done.scalars().fetchall())
    ui_not_complete = list(ui_not_complete.scalars().fetchall())
    ui_not_date = list(ui_not_date.scalars().fetchall())
    ui_with_notifications_on = list(
        ui_with_notifications_on.scalars().fetchall()
    )

    users_needs_notifications = set(ui_not_count_done).intersection(
        set(ui_not_complete + ui_not_date)
    )
    users_needs_notifications = set(ui_with_notifications_on).intersection(
        users_needs_notifications
    )

    return list(users_needs_notifications)


async def myfunc(my_bot: AsyncTeleBot):
    """Отправляет сообщение пользователям"""
    async with session_async() as session:
        users_id = await get_users_id(session)

        for user_id in users_id:
            await my_bot.send_message(
                chat_id=int(user_id),
                text="Добрый день!\nНе забудьте выполнить ваши привычки сегодня🍀",
            )


async def main():
    """
    Ежедневно в 12 выполняет отправку уведомлений
    Пользователь получает уведомление если
    1) в таблице HabitsDB есть хотя-бы одна привычка с count_done < days_to_form
     1.1) если у пользователя в таблице HabitsTodayDB есть привычка с сегодняшней датой и с complete == None
          или
     1.2) если у пользователя в таблице HabitsTodayDB отсутствует привычка с сегодняшней датой
    2) если у пользователя включены уведомления
    """
    scheduler.add_job(
        myfunc, "cron", hour=12, id="my_job_id", kwargs={"my_bot": bot}
    )
    scheduler.start()
    while True:
        await asyncio.sleep(1000)


if __name__ == "__main__":
    asyncio.run(main())
