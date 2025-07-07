import asyncio
import datetime
import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from telebot.async_telebot import AsyncTeleBot

from bot.loader import bot
from app.database import session_async, UsersDB
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database import HabitsDB
from database import HabitsTodayDB

scheduler = AsyncIOScheduler()


async def get_habits_incomplete(session: AsyncSession) -> list[HabitsDB]:
    habits_incomplete = await session.execute(
        select(HabitsDB).where(HabitsDB.count_done < 21)
    )
    return list(habits_incomplete.scalars().fetchall())

async def get_habits_not_in_table_with_today_date(session: AsyncSession, date_today):
    habits = await session.execute(select(HabitsTodayDB).where(HabitsTodayDB.date < date_today))
    return habits.scalars().fetchall()


async def get_habits_noncomplete_today(session: AsyncSession) -> list[HabitsTodayDB]:
    habits = await session.execute(select(HabitsTodayDB).where(HabitsTodayDB.completed == None))
    return list(habits.scalars().fetchall())


async def get_users(session: AsyncSession) -> list[UsersDB]:
    users = await session.execute(select(UsersDB)
                                  .options(selectinload(UsersDB.habits), selectinload(UsersDB.today_habits)))
    return list(users.scalars().fetchall())


async def get_users_id_from_habits_db(session: AsyncSession):
    users_id = await session.execute(
        select(HabitsDB.user_id).where(HabitsDB.count_done < 21)
    )
    return list(users_id.scalars().fetchall())


async def get_users_id_from_habits_today_db(session: AsyncSession, date):
    users_id = await session.execute(
        select(HabitsTodayDB.user_id).where(HabitsTodayDB.completed == None, HabitsTodayDB.date < date)
    )
    return list(users_id.scalars().fetchall())


async def get_users_id(session: AsyncSession):
    date = datetime.datetime.now().date()
    # 1) в таблице HabitsDB есть хотя-бы одна привычка с count_done < 21
    ui_not_count_done = await session.execute(select(HabitsDB.user_id).where(HabitsDB.count_done < 21))

    # 1.1) если у пользователя в таблице HabitsTodayDB есть привычка с сегодняшней датой и с complete == None
    ui_not_complete = await session.execute(
        select(HabitsTodayDB.user_id)
        .where(
            HabitsTodayDB.date == date,
            HabitsTodayDB.completed == None,)
    )

    # 1.2) если у пользователя в таблице HabitsTodayDB отсутствует привычка с сегодняшней датой
    ui_not_date = await session.execute(
        select(HabitsDB.user_id, HabitsTodayDB)
        .join(HabitsTodayDB, HabitsDB.id == HabitsTodayDB.habit_id, isouter=True)
        .where(HabitsTodayDB.date == None)

    )

    ui_not_count_done = list(ui_not_count_done.scalars().fetchall())
    ui_not_complete = list(ui_not_complete.scalars().fetchall())
    ui_not_date = list(ui_not_date.scalars().fetchall())

    print("ui_not_count_done", set(ui_not_count_done))
    print("ui_not_complete + ui_not_date", set(ui_not_complete + ui_not_date))
    print("пересечение", set(ui_not_count_done).intersection(set(ui_not_complete + ui_not_date)))

    # for i,o in ui_not_date:
    #     print(i, o)

async def myfunc(my_bot: AsyncTeleBot):
    async with session_async() as session:
        await get_users_id(session)


async def main():

    # пользователь получает уведомление если
    # 1) в таблице HabitsDB есть хотя-бы одна привычка с count_done < 21
    #  1.1) если у пользователя в таблице HabitsTodayDB есть привычка с сегодняшней датой и с complete == None
    #  или
    #  1.2) если у пользователя в таблице HabitsTodayDB отсутствует привычка с сегодняшней датой
    scheduler.add_job(myfunc,
                      'interval',
                      seconds=5,
                      id='my_job_id',
                      kwargs={'my_bot': bot}
                      )
    scheduler.start()
    while True:
        await asyncio.sleep(1000)


if __name__ == "__main__":
    asyncio.run(main())

