from pydantic import BaseModel


class Habit(BaseModel):
    name: str
    count_done: int = 0
    user_id: str


class HabitResponse(BaseModel):
    name: str


class HabitId(BaseModel):
    habit_id: str
