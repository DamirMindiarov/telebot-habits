FROM python:3.12-alpine

COPY /app/ /new_telebot_habits/app

COPY handlers /new_telebot_habits/handlers
COPY .env /new_telebot_habits/
COPY config.py /new_telebot_habits/
COPY functions.py /new_telebot_habits/
COPY loader.py /new_telebot_habits/
COPY main.py /new_telebot_habits/
COPY notifications.py /new_telebot_habits/
COPY states.py /new_telebot_habits/
#COPY /bot/ /new_telebot_habits/bot

COPY .gitignore /new_telebot_habits/
COPY mytest.py /new_telebot_habits/
COPY poetry.lock /new_telebot_habits/
COPY pyproject.toml /new_telebot_habits/




WORKDIR /new_telebot_habits/

#RUN pip install --upgrade pip wheel "poetry==2.1.3"
RUN pip install "poetry==2.1.3"
RUN poetry config virtualenvs.create false
RUN poetry install

#RUN pip install -r requirements.txt