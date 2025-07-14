from pydantic import BaseModel


# class Token(BaseModel):
#     token: str
#     token_type: str
#
#
# class User(BaseModel):
#     id: int
#     username: str
#     hashed_password: str


class UserId(BaseModel):
    user_id: str
