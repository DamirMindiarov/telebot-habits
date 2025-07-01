import datetime
import time

from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import defer

from database import session_async, UsersDB, HabitsDB, HabitsTodayDB


async def get_habits_by_user_id(user_id: str, session: AsyncSession) -> list[
    HabitsDB]:
    habits = await session.execute(
        select(HabitsDB).where(UsersDB.user_id == user_id))
    return list(habits.scalars().fetchall())


async def add_habit(name: str, count_done: int, user_id: str,
                    session: AsyncSession) -> HabitsDB:
    habit: HabitsDB = HabitsDB(name=name, count_done=count_done,
                               user_id=user_id)
    session.add(habit)

    return habit


async def add_habit_today(habit_id: int, session: AsyncSession):
    habit_today: HabitsTodayDB = HabitsTodayDB(
        habit_id=habit_id,
        date=datetime.datetime.now().date()
    )
    session.add(habit_today)

    return


async def del_habit(habit_id: int, session: AsyncSession):
    await session.execute(delete(HabitsDB).where(HabitsDB.id == habit_id))


async def update_habit(habit_id: int, habit_new_name: str,
                       session: AsyncSession):
    await session.execute(
        update(HabitsDB)
        .where(HabitsDB.id == habit_id)
        .values(name=habit_new_name)
    )


async def get_habits_today_by_user_id(user_id: str, session: AsyncSession) -> \
list[tuple]:
    # удаляю все привычки всех пользователей на вчера
    # await session.execute(
    #     delete(HabitsTodayDB).where(HabitsTodayDB.date < date)
    # )

    # беру из таблицы HabitsTodayDB все привычки этого пользователя

    habits_today = await session.execute(
        select(HabitsDB.id, HabitsDB.name, HabitsTodayDB.completed).
        join(HabitsTodayDB).
        where(HabitsDB.user_id == user_id)
    )

    habits_today = [tuple(habit_today) for habit_today in
                    habits_today.fetchall()]
    return habits_today


async def from_habits_into_habits_today(user_id: str, session: AsyncSession):
    habits: list[HabitsDB] = await get_habits_by_user_id(user_id,
                                                         session=session)
    list_habits_id = [habit.id for habit in habits if habit.count_done < 21]

    for habit_id in list_habits_id:
        try:
            await add_habit_today(habit_id=habit_id, session=session)
        except IntegrityError:
            continue


async def delete_old_habits_from_today_habits(session: AsyncSession) -> bool:
    date = datetime.datetime.now().date()

    result = await session.execute(
        delete(HabitsTodayDB).where(HabitsTodayDB.date < date)
    )
    return True if result else False


async def check_date_habits_today(session: AsyncSession) -> bool:
    date = datetime.datetime.now().date()
    result = await session.execute(select(HabitsTodayDB).where(HabitsTodayDB.date == date))
    result = result.scalars().fetchall()
    return False if result else True


async def update_completed_habits_today_by_habit_id(habit_id: int, session: AsyncSession):
    await session.execute(
        update(HabitsTodayDB).where(HabitsTodayDB.habit_id == habit_id).values(completed=True)
    )
    return

async def update_count_done(habit_id: int, session: AsyncSession):
    await session.execute(
        update(HabitsDB).where(HabitsDB.id == habit_id)
        .values(count_done=HabitsDB.count_done + 1)
    )
    return