from fastapi import Depends, APIRouter

from authorization.functions import get_current_user, refresh_token
from authorization.pydentic_models import User
from functions import get_habits_by_user_id, add_habit, del_habit
from app.pydentic_models import Habit, HabitId, HabitResponse

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

    return HabitResponse(name=added_habit.name)


@router.delete("/habits")
async def del_habits(habit_id: HabitId, current_user: User = Depends(get_current_user)):
    current_user = await current_user
    await refresh_token(user_id=current_user.user_id)
    await del_habit(habit_id=int(habit_id.habit_id))
    return








#
#
# @router.post("/test_token")
# async def test_token(current_user: User = Depends(get_current_user)):
#     current_user = await current_user
#     await refresh_token(user_id=current_user.user_id)
#     return current_user
