import datetime

from sqlalchemy import select, delete, update
from sqlalchemy.orm import defer

from database import session_async, UsersDB, HabitsDB, HabitsTodayDB


async def get_habits_by_user_id(user_id: str) -> str:
    async with session_async() as session:
        habits = await session.execute(
            select(HabitsDB).where(UsersDB.user_id == user_id))

    return habits.scalars().fetchall()


async def add_habit(name: str, count_done: int, user_id: str) -> HabitsDB:
    habit: HabitsDB = HabitsDB(name=name, count_done=count_done,
                               user_id=user_id)

    async with session_async() as session:
        session.add(habit)
        await session.commit()

    return habit


async def add_habit_today(habit_id: int):
    habit_today: HabitsTodayDB = HabitsTodayDB(
        habit_id=habit_id,
        date=datetime.datetime.now().date()
    )
    async with session_async() as session:
        session.add(habit_today)
        await session.commit()

    return


async def del_habit(habit_id: int):
    async with session_async() as session:
        await session.execute(delete(HabitsDB).where(HabitsDB.id == habit_id))
        await session.commit()


async def update_habit(habit_id: int, habit_new_name: str):
    async with session_async() as session:
        await session.execute(
            update(HabitsDB)
            .where(HabitsDB.id == habit_id)
            .values(name=habit_new_name)
        )
        await session.commit()


async def get_habits_today_by_user_id(user_id: str) -> list[tuple]:
    date = datetime.datetime.now().date()

    async with session_async() as session:
        # удаляю все привычки всех пользователей на вчера
        await session.execute(
            delete(HabitsTodayDB).where(HabitsTodayDB.date < date)
        )
        await session.commit()

        # беру из таблицы HabitsTodayDB все привычки этого пользователя
        habits_today = await session.execute(
            select(HabitsDB.id, HabitsDB.name, HabitsTodayDB.completed).
            join(HabitsTodayDB).
            where(HabitsDB.user_id == user_id)
        )
    habits_today = habits_today.fetchall()
    return habits_today
