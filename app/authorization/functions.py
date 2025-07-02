from datetime import timedelta, timezone, datetime

import jwt
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.authorization.config import (
    pwd_context,
    SECRET_KEY,
    ALGORITHM,
    TOKEN_EXPIRE_MINUTES,
)
from app.database import session_async, UsersDB


def verify_password(password: str, hashed_password: str) -> bool:
    """Проверяет соответствие паролей"""
    return pwd_context.verify(password, hashed_password)


async def get_user(username: str, session: AsyncSession) -> UsersDB:
    """Возвращает пользователя по username"""
    user = await session.execute(
        select(UsersDB)
        .where(UsersDB.user_id == username)
        .options(
            selectinload(UsersDB.habits), selectinload(UsersDB.today_habits)
        )
    )

    return user.scalar()


async def authenticate_user(
    username: str, password: str, session: AsyncSession
) -> UsersDB | bool:
    """Проверяет подлинность пользователя"""
    user = await get_user(username, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_token(username: str, expires_delta: timedelta) -> str:
    """Создает токен"""
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"username": username, "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def add_user(username: str, hashed_password: str) -> UsersDB:
    """Добавляет пользователя в БД"""
    user = UsersDB(user_id=username, hashed_password=hashed_password)
    async with session_async() as session:
        session.add(user)
        await session.commit()
    return user


async def get_current_user(token: str, session: AsyncSession) -> UsersDB:
    """Проверяет токен на актуальность, возвращает пользователя"""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credential_exception
    user = await get_user(payload["username"], session)
    return user


async def refresh_token(user_id: str, session: AsyncSession):
    """Обновляет токен"""
    timedelta_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    token = create_token(
        username=user_id, expires_delta=timedelta_token_expires
    )
    await session.execute(
        update(UsersDB).where(UsersDB.user_id == user_id).values(token=token)
    )


async def update_password(password: str, user_id: str):
    """Обновляет пароль"""
    hashed_password = pwd_context.hash(password)
    async with session_async() as session:
        await session.execute(
            update(UsersDB)
            .where(UsersDB.user_id == user_id)
            .values(hashed_password=hashed_password)
        )
        await session.commit()


async def token_is_alive(token: str) -> bool:
    """Проверяет актуальность токена"""
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        return False
    return True
