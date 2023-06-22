from models import User, Messages, Product, Order, Order_items, Payment
import time
from datetime import datetime
from loader import session


def get_user_id(telegram_id):
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    return user


# print(get_user_id(345345345))


def add_user(telegram_id, user_name, full_name, date):
    new_user = User(
        telegram_id=telegram_id,
        user_name=user_name,
        full_name=full_name,
        # registration_date = date
        balance=0,
        actyvity=False
    )
    session.add(new_user)
    session.commit()


def add_message(message):
    telegram_id = message.chat.id
    user_name = message.chat.username
    full_name = message.chat.full_name
    text_message = message.text
    date = message.date

    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    if user is None:
        add_user(telegram_id, user_name, full_name, date)
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
    new_message = Messages(
        telegram_id = user.telegram_id,
        # date=date,
        text_message=text_message
    )
    session.add(new_message)
    session.commit()



