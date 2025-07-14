from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from .pydentic_models import UserId

from .config import pwd_context
from .functions import (
    authenticate_user,
    refresh_token,
    add_user,
)
from authorization.database import session_async, UsersDB

router = APIRouter()


@router.post("/token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Добавляет токен в БД (Авторизация пользователя)"""
    async with session_async() as session:
        user = await authenticate_user(
            form_data.username, form_data.password, session
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        await refresh_token(user_id=user.user_id, session=session)
        await session.commit()

    return


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def registration_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Регистрирует нового пользователя"""
    user = await add_user(
        form_data.username, pwd_context.hash(form_data.password)
    )
    return user


@router.get("/user/token")
async def get_user_token(user_id: UserId):
    """"""

    async with session_async() as session:
        token = await session.execute(
            select(UsersDB.token).where(UsersDB.user_id == user_id.user_id)
        )
        token = token.scalar()

    return token