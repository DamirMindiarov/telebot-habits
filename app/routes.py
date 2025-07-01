from fastapi import Depends, APIRouter

from authorization.functions import get_current_user, refresh_token
from authorization.pydentic_models import User
from app.functions import get_habits_by_user_id, add_habit, del_habit, update_habit, add_habit_today, get_habits_today_by_user_id, from_habits_into_habits_today, delete_old_habits_from_today_habits, check_date_habits_today, update_completed_habits_today_by_habit_id, update_count_done
from app.pydentic_models import Habit, HabitId, HabitResponse, HabitUpdate, HabitToday
from database import session_async
from functions import check_completed_habits_today

router = APIRouter()


@router.get("/habits")
async def get_habits(current_user: User = Depends(get_current_user)):
    current_user = await current_user

    async with session_async() as session:
        habits = await get_habits_by_user_id(user_id=current_user.user_id, session=session)

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return habits


@router.post("/habits")
async def add_habits(habit: Habit, current_user: User = Depends(get_current_user)) -> HabitResponse:
    current_user = await current_user

    async with session_async() as session:
        added_habit = await add_habit(name=habit.name, count_done=habit.count_done, user_id=habit.user_id, session=session)
        await session.flush()
        await add_habit_today(habit_id=int(added_habit.id), session=session)

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return HabitResponse(name=added_habit.name)


@router.delete("/habits")
async def del_habits(habit_id: HabitId, current_user: User = Depends(get_current_user)):
    current_user = await current_user

    async with session_async() as session:
        await del_habit(habit_id=int(habit_id.habit_id), session=session)

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()
    return


@router.put("/habits")
async def update_habits(habit: HabitUpdate, current_user: User = Depends(get_current_user)):
    current_user = await current_user

    async with session_async() as session:
        await update_habit(habit_id=int(habit.habit_id), habit_new_name=habit.habit_new_name, session=session)

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return


@router.get("/habits/today")
async def get_habits_today(current_user: User = Depends(get_current_user)) -> list[HabitToday]:
    current_user = await current_user

    async with session_async() as session:
        await delete_old_habits_from_today_habits(session=session)

        if await check_date_habits_today(session=session):
            await from_habits_into_habits_today(user_id=current_user.user_id, session=session)

        habits_today = await get_habits_today_by_user_id(user_id=current_user.user_id, session=session)
        habits_today = [HabitToday(id=habit[0], name=habit[1], completed=habit[2]) for habit in habits_today]

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return habits_today


@router.put("/habits/today")
async def route_habit_today_done(habit_id: HabitId, current_user: User = Depends(get_current_user)):
    current_user = await current_user
    text = None

    async with session_async() as session:
        habit_already_completed_today = await check_completed_habits_today(habit_id=int(habit_id.habit_id), session=session)

        if not habit_already_completed_today:
            await update_completed_habits_today_by_habit_id(habit_id=int(habit_id.habit_id), session=session)
            await update_count_done(habit_id=int(habit_id.habit_id), session=session)
            text = "completed"

        await refresh_token(user_id=current_user.user_id, session=session)
        await session.commit()

    return text



# @router.post("/test_token")
# async def test_token(current_user: User = Depends(get_current_user)):
#     current_user = await current_user
#     await refresh_token(user_id=current_user.user_id)
#     return current_user
