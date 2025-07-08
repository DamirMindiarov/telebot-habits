from pydantic import BaseModel


class Habit(BaseModel):
    name: str
    count_done: int = 0
    user_id: str


class HabitResponse(BaseModel):
    name: str


class HabitId(BaseModel):
    habit_id: str


class HabitUpdate(HabitId):
    habit_new_name: str


class HabitToday(BaseModel):
    habit_id: int
    name: str
    completed: bool | None


class DaysToForm(BaseModel):
    days: int
