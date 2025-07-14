import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

db_url_async = "postgresql+asyncpg://admin:admin@database:5432/habits"

engine_async = create_async_engine(url=db_url_async, echo=False)

session_async = async_sessionmaker(bind=engine_async, expire_on_commit=False)


async def create_db():
    """Создает таблицы в БД"""
    async with engine_async.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


class Base(AsyncAttrs, DeclarativeBase):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UsersDB(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    token: Mapped[str] = mapped_column(nullable=True)
    notifications: Mapped[str] = mapped_column(default="+")

    habits: Mapped[list["HabitsDB"]] = relationship(
        "HabitsDB", back_populates="user"
    )
    today_habits: Mapped[list["HabitsTodayDB"]] = relationship(
        "HabitsTodayDB", back_populates="user"
    )


class HabitsDB(Base):
    __tablename__ = "habits"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    count_done: Mapped[int]
    days_to_form: Mapped[int] = mapped_column(default=21)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))

    user: Mapped["UsersDB"] = relationship("UsersDB", back_populates="habits")



class HabitsTodayDB(Base):
    __tablename__ = "habits_today"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    completed: Mapped[bool] = mapped_column(nullable=True)
    date: Mapped[datetime.date]
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"), unique=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))

    user: Mapped["UsersDB"] = relationship(
        "UsersDB", back_populates="today_habits"
    )

