import datetime

from fastapi import Depends, APIRouter

from app.database import session_async, HabitsDB, HabitsTodayDB
from app.functions import (
    del_habit,
    delete_old_habits_from_today_habits,
    check_date_habits_today,
)
from app.pydentic_models import (
    Habit,
    HabitId,
    HabitResponse,
    HabitUpdate,
    HabitToday,
)
from authorization.config import oauth2_scheme
from authorization.functions import get_current_user, refresh_token
from functions import check_completed_habits_today

router = APIRouter()


@router.get("/habits")
async def get_habits(token: str = Depends(oauth2_scheme)) -> list[HabitsDB]:
    """Возвращает список привычек пользователя"""
    async with session_async() as session:
        current_user = await get_current_user(token, session)

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return current_user.habits


@router.post("/habits")
async def add_habits(
    habit: Habit, token: str = Depends(oauth2_scheme)
) -> HabitResponse:
    """Добавляет привычку в БД"""
    new_habit = HabitsDB(
        name=habit.name, count_done=habit.count_done, user_id=habit.user_id
    )

    async with session_async() as session:
        current_user = await get_current_user(token, session)
        current_user.habits.append(new_habit)
        await session.flush()

        new_habit_today = HabitsTodayDB(
            date=datetime.datetime.now().date(),
            habit_id=current_user.habits[-1].id,
            user_id=habit.user_id,
            name=current_user.habits[-1].name,
        )
        current_user.today_habits.append(new_habit_today)

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return HabitResponse(name=current_user.habits[-1].name)


@router.delete("/habits")
async def del_habits(habit_id: HabitId, token: str = Depends(oauth2_scheme)):
    """Удаляет привычку"""
    deleted_habit = None

    async with session_async() as session:
        current_user = await get_current_user(token, session)
        for habit in current_user.habits:
            if habit.id == int(habit_id.habit_id):
                deleted_habit = await del_habit(
                    habit_id=int(habit_id.habit_id), session=session
                )

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()
    return deleted_habit


@router.put("/habits")
async def update_habits(
    new_habit: HabitUpdate, token: str = Depends(oauth2_scheme)
):
    """Изменяет привычку в HabitsTodayDB и HabitsDB"""
    updated_habit = None

    async with session_async() as session:
        current_user = await get_current_user(token, session)

        for habit in current_user.habits:
            if habit.id == int(new_habit.habit_id):
                habit.name = new_habit.habit_new_name
                updated_habit = habit

        for habit in current_user.today_habits:
            if habit.id == int(new_habit.habit_id):
                habit.name = new_habit.habit_new_name

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return updated_habit


@router.get("/habits/today")
async def get_habits_today(
    token: str = Depends(oauth2_scheme),
) -> list[HabitToday]:
    """Возвращает список привычек, которые нужно сегодня выполнить"""
    habits_today = []
    async with session_async() as session:
        current_user = await get_current_user(token, session)

        await delete_old_habits_from_today_habits(session=session)

        if await check_date_habits_today(session=session):
            less_then_21 = [
                habit for habit in current_user.habits if habit.count_done < 21
            ]
            for habit in less_then_21:
                habit_today = HabitsTodayDB(
                    date=datetime.datetime.now().date(),
                    habit_id=habit.id,
                    user_id=habit.user_id,
                )
                current_user.today_habits.append(habit_today)

        habits_today = [
            HabitToday(id=habit.id, name=habit.name, completed=habit.completed)
            for habit in current_user.today_habits
        ]

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return habits_today


@router.put("/habits/today")
async def route_habit_today_done(
    habit_id: HabitId, token: str = Depends(oauth2_scheme)
) -> None | str:
    """Отмечает в таблице HabitsTodayDB, что привычка выполнена"""
    text = None

    async with session_async() as session:
        current_user = await get_current_user(token, session)
        habit_already_completed_today = await check_completed_habits_today(
            habit_id=int(habit_id.habit_id), session=session
        )

        if not habit_already_completed_today:
            for habit in current_user.today_habits:
                if habit.id == int(habit_id.habit_id):
                    habit.completed = True
                    text = "completed"

            for habit in current_user.habits:
                if habit.id == int(habit_id.habit_id):
                    habit.count_done += 1

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return text
