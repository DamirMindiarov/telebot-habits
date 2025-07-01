from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.authorization.functions import authenticate_user, refresh_token, \
    add_user, get_current_user
from app.authorization.config import pwd_context
from authorization.pydentic_models import User
from database import session_async

router = APIRouter()


@router.post("/token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    async with session_async() as session:
        user = await authenticate_user(form_data.username, form_data.password, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        await refresh_token(user_id=user.user_id, session=session)
        await session.commit()

    return


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def registration_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await add_user(form_data.username,
                          pwd_context.hash(form_data.password))
    return user
