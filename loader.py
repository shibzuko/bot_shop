from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)

# Создание соединения с базой данных
engine = create_engine('sqlite:///DataBase.db')

# Создание сессии
Session = sessionmaker(bind=engine)

session = Session()

# Объявление базового класса для моделей
Base = declarative_base()

# Создание dispatcher с использованием MemoryStorage
dp = Dispatcher(bot, storage=MemoryStorage())

