import sqlalchemy as db
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

TOKEN = str(getenv('TOKEN'))

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

# database init
engine = db.create_engine('sqlite:///subscribe_database.db')
connectio = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()
metadata = db.MetaData()

# subscribers table
subscribers = db.Table('subscribers', metadata,
                       db.Column('id', db.Integer, primary_key=True),
                       db.Column('user_id', db.Integer),
                       db.Column('user_fullname', db.Text),
                       db.Column('end_data', db.Date))

# subscriptions table
subscriptions = db.Table('subscriptions', metadata,
                         db.Column('id', db.Integer, primary_key=True),
                         db.Column('subsription_name', db.Text),
                         db.Column('duration', db.Integer),
                         db.Column('price', db.Float))

Base = declarative_base()


# connectio.execute(subscriptions.insert().values(subsription_name='подписка на 1 месяц',
#                                                 duration='1',
#                                                 price='500'))
# connectio.execute(subscriptions.insert().values(subsription_name='подписка на 2 месяц',
#                                                 duration='2',
#                                                 price='1000'))
connectio.commit()

metadata.create_all(engine)
