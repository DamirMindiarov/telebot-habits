import datetime

from sqlalchemy import select, delete, CursorResult, update
from sqlalchemy.ext.asyncio.session import AsyncSession

from authorization.database import HabitsDB, HabitsTodayDB


async def del_habit(habit_id: int, session: AsyncSession) -> CursorResult:
    """Удаляет привычку из HabitsTodayDB и HabitsDB по ее id"""
    await session.execute(
        delete(HabitsTodayDB).where(HabitsTodayDB.habit_id == habit_id)
    )
    await session.commit()
    habit = await session.execute(
        delete(HabitsDB).where(HabitsDB.id == habit_id)
    )
    return habit


async def delete_old_habits_from_today_habits(session: AsyncSession):
    """Удаляет старые(чья дата меньше текущей) привычки из таблицы "На сегодня(HabitsTodayDB)" """
    date = datetime.datetime.now().date()

    await session.execute(
        delete(HabitsTodayDB).where(HabitsTodayDB.date < date)
    )

    return


async def check_date_habits_today(session: AsyncSession) -> bool:
    """Проверяет есть ли привычки в таблице HabitsTodayDB с текущей датой"""
    date = datetime.datetime.now().date()
    result = await session.execute(
        select(HabitsTodayDB).where(HabitsTodayDB.date == date)
    )
    result = result.scalars().fetchall()
    return False if result else True


async def check_completed_habits_today(
    habit_id: int, session: AsyncSession
) -> bool:
    """Проверяет выполнена ли привычка в таблице HabitsTodayDB"""
    result = await session.execute(
        select(HabitsTodayDB).where(
            HabitsTodayDB.habit_id == habit_id, HabitsTodayDB.completed == True
        )
    )
    result = result.scalars().fetchall()
    return True if result else False


async def update_count_days_for_habits_by_user_id(
    user_id: str, days: int, session: AsyncSession
):
    """Обновляет колонку days_to_form в таблице Habits"""
    await session.execute(
        update(HabitsDB)
        .where(HabitsDB.user_id == user_id)
        .values(days_to_form=days)
    )
