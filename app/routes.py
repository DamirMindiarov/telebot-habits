from fastapi import Depends, APIRouter

from authorization.functions import get_current_user, refresh_token
from authorization.pydentic_models import User
from app.functions import get_habits_by_user_id, add_habit, del_habit, update_habit, add_habit_today, get_habits_today_by_user_id, from_habits_into_habits_today
from app.pydentic_models import Habit, HabitId, HabitResponse, HabitUpdate, HabitToday
from database import session_async

router = APIRouter()


@router.get("/habits")
async def get_habits(current_user: User = Depends(get_current_user)):
    current_user = await current_user
    habits = await get_habits_by_user_id(user_id=current_user.user_id)
    return habits


@router.post("/habits")
async def add_habits(habit: Habit, current_user: User = Depends(get_current_user)) -> HabitResponse:
    current_user = await current_user
    await refresh_token(user_id=current_user.user_id)

    added_habit = await add_habit(name=habit.name, count_done=habit.count_done, user_id=habit.user_id)
    await add_habit_today(habit_id=added_habit.id)

    return HabitResponse(name=added_habit.name)


@router.delete("/habits")
async def del_habits(habit_id: HabitId, current_user: User = Depends(get_current_user)):
    current_user = await current_user
    await refresh_token(user_id=current_user.user_id)
    await del_habit(habit_id=int(habit_id.habit_id))
    return


@router.put("/habits")
async def update_habits(habit: HabitUpdate, current_user: User = Depends(get_current_user)):
    current_user = await current_user
    await refresh_token(user_id=current_user.user_id)
    await update_habit(habit_id=int(habit.habit_id), habit_new_name=habit.habit_new_name)

    return


@router.get("/habits/today")
async def get_habits_today(current_user: User = Depends(get_current_user)) -> list[HabitToday]:
    current_user = await current_user
    await refresh_token(user_id=current_user.user_id)
    habits_today = await get_habits_today_by_user_id(user_id=current_user.user_id)
    habits_today = [HabitToday(id=habit[0], name=habit[1], completed=habit[2]) for habit in habits_today]

    await from_habits_into_habits_today(user_id=current_user.user_id)


    return habits_today





#
#
# @router.post("/test_token")
# async def test_token(current_user: User = Depends(get_current_user)):
#     current_user = await current_user
#     await refresh_token(user_id=current_user.user_id)
#     return current_user
