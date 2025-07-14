import datetime

from fastapi import Depends, APIRouter
from sqlalchemy.exc import IntegrityError

from authorization.database import session_async, HabitsDB, HabitsTodayDB
from functions import (
    del_habit,
    delete_old_habits_from_today_habits,
    update_count_days_for_habits_by_user_id,
)
from pydentic_models import (
    Habit,
    HabitId,
    HabitResponse,
    HabitUpdate,
    HabitToday,
    DaysToForm,
)
from authorization.config import oauth2_scheme
from authorization.functions import get_current_user, refresh_token
from functions import check_completed_habits_today

router = APIRouter()


@router.get("/habits")
async def get_habits(token: str = Depends(oauth2_scheme)):
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

    async with session_async() as session:
        current_user = await get_current_user(token, session)

        if len(current_user.habits):
            days_to_form = int(current_user.habits[0].days_to_form)
        else:
            days_to_form = 21

        new_habit = HabitsDB(
            name=habit.name,
            count_done=habit.count_done,
            days_to_form=days_to_form,
            user_id=habit.user_id,
        )
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
                # deleted_habit = await session.delete(habit_id)
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
            if habit.habit_id == int(new_habit.habit_id):
                habit.name = new_habit.habit_new_name

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return updated_habit


@router.get("/habits/today")
async def get_habits_today(token=Depends(oauth2_scheme)) -> list:
    """Возвращает список привычек, которые нужно сегодня выполнить"""
    habits_today = []
    async with session_async() as session:
        await delete_old_habits_from_today_habits(session=session)
        current_user = await get_current_user(token, session)

        if not current_user.today_habits:
            less_then_21 = [
                habit for habit in current_user.habits if habit.count_done < 21
            ]

            try:
                for habit in less_then_21:
                    habit_today = HabitsTodayDB(
                        name=habit.name,
                        date=datetime.datetime.now().date(),
                        habit_id=habit.id,
                        user_id=habit.user_id,
                    )
                    current_user.today_habits.append(habit_today)
            except IntegrityError:
                pass

        habits_today = [
            HabitToday(
                habit_id=habit.habit_id,
                name=habit.name,
                completed=habit.completed,
            )
            for habit in current_user.today_habits
        ]

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return habits_today


@router.put("/habits/today")
async def route_habit_today_done(
    habit_id: HabitId, token: str = Depends(oauth2_scheme)
):
    """Отмечает в таблице HabitsTodayDB, что привычка выполнена"""
    text = None

    async with session_async() as session:
        current_user = await get_current_user(token, session)
        habit_already_completed_today = await check_completed_habits_today(
            habit_id=int(habit_id.habit_id), session=session
        )

        if not habit_already_completed_today:
            for habit in current_user.today_habits:
                if habit.habit_id == int(habit_id.habit_id):
                    habit.completed = True
                    text = "completed"

            for habit in current_user.habits:
                if habit.id == int(habit_id.habit_id):
                    habit.count_done += 1

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return text


@router.put("/habits/notifications")
async def notifications(token: str = Depends(oauth2_scheme)) -> str:
    """
    Переключает состояние уведомлений с "получать" на "не получать" и наоборот.
    """
    async with session_async() as session:
        current_user = await get_current_user(token, session)

        if current_user.notifications == "+":
            current_user.notifications = "-"
            result = "Отключено"
        elif current_user.notifications == "-":
            current_user.notifications = "+"
            result = "Включено"

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return result


@router.put("/habit/count_days")
async def update_count_days(
    days: DaysToForm, token: str = Depends(oauth2_scheme)
):
    """Обновляет колонку days_to_form в таблице Habits"""
    async with session_async() as session:
        current_user = await get_current_user(token, session)

        await update_count_days_for_habits_by_user_id(
            user_id=current_user.user_id, days=days.days, session=session
        )

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return
