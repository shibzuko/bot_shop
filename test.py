from models import User, Message, Product, Order, Order_items, Payment, session
import time
from datetime import datetime

def add_user(telegram_id, user_name, full_name, date):
    new_user = User(
        telegram_id=telegram_id,
        user_name=user_name,
        full_name=full_name,
        # registration_date = date
        balance=0,
        actyvity = False
    )
    session.add(new_user)
    session.commit()





def get_user_id(telegram_id):
    us = session.query(User).filter_by(telegram_id=telegram_id).first()
    return us


print(get_user_id(345345345))