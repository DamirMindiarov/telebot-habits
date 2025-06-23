from fastapi import Depends, HTTPException, status
from datetime import timedelta, timezone, datetime
import jwt
from jwt.exceptions import InvalidTokenError

from app.database import session_async, UsersDB
from sqlalchemy import select, update
from app.authorization.config import pwd_context, SECRET_KEY, ALGORITHM, oauth2_scheme, TOKEN_EXPIRE_MINUTES


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


async def get_user(username: str):
    async with session_async() as session:
        user = await session.execute(select(UsersDB).where(UsersDB.user_id == username))
    return user.scalar()


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_token(username: str, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"username": username, "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def add_user(username: str, hashed_password: str):
    user = UsersDB(user_id=username, hashed_password=hashed_password)
    async with session_async() as session:
        session.add(user)
        await session.commit()
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credential_exception
    user = get_user(payload["username"])
    return user


async def refresh_token(user_id: str):
    timedelta_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    token = create_token(username=user_id,
                         expires_delta=timedelta_token_expires)
    async with session_async() as session:
        await session.execute(update(UsersDB).where(UsersDB.user_id == user_id).values(token=token))
        await session.commit()


async def update_password(password: str, user_id: str):
    hashed_password = pwd_context.hash(password)
    async with session_async() as session:
        await session.execute(update(UsersDB).where(UsersDB.user_id == user_id).values(hashed_password=hashed_password))
        await session.commit()


async def token_is_alive(token: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        return False
    return True