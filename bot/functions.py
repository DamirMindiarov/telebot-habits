from sqlalchemy import select

from app.database import session_async, UsersDB, HabitsDB


async def get_token_by_user_id(user_id: str) -> str:
    async with session_async() as session:
        res = await session.execute(
            select(UsersDB.token).where(UsersDB.user_id == user_id))
        res = res.scalar()
        return res


