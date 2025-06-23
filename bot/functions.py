from sqlalchemy import select

from app.database import session_async, UsersDB, HabitsDB
from authorization.functions import get_current_user, token_is_alive


async def get_token_by_user_id(user_id: str) -> str:
    async with session_async() as session:
        res = await session.execute(
            select(UsersDB.token).where(UsersDB.user_id == user_id))
        res = res.scalar()
        return res


async def check_auth(user_id: int):
    token = await get_token_by_user_id(user_id=str(user_id))
    response = await token_is_alive(token=token)
    return token if response else False


