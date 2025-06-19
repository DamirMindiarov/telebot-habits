from fastapi import Depends, APIRouter

from authorization.functions import get_current_user, refresh_token
from authorization.pydentic_models import User
from functions import get_habits_by_user_id

router = APIRouter()


@router.get("/habits")
async def get_habits(current_user: User = Depends(get_current_user)):
    current_user = await current_user
    habits = await get_habits_by_user_id(user_id=current_user.user_id)
    print(habits)
    return habits


# @router.post("/habits")
# async def add_habits(current_user: User = Depends(get_current_user)):
#     current_user = await current_user
#     await refresh_token(user_id=current_user.user_id)
#     return current_user
#
#
# @router.post("/test_token")
# async def test_token(current_user: User = Depends(get_current_user)):
#     current_user = await current_user
#     await refresh_token(user_id=current_user.user_id)
#     return current_user
