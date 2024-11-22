import psycopg2
import sqlalchemy
from typing import List
from sqlalchemy import String, Date, ForeignKey, Integer, URL, create_engine, select, func, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from dotenv import load_dotenv
from datetime import date
from datetime import datetime
from faker import Faker
import os
from itertools import islice

# from  models import *
from models import *
import models
from engine import *

def create_database() -> None:
    models.Base.metadata.create_all(engine)

def drop_database() -> None:
    models.Base.metadata.drop_all(engine)

def reset_database() -> None:
    drop_database()
    create_database()


def create_user(first_name, last_name, birth_date, email, gender):
    with Session(engine) as session:
        user = User(
            first_name = first_name,
            last_name = last_name,
            birth_date = birth_date,
            email = email, 
            gender = gender
        ) 
        session.add(user)
        session.commit()

def find_user_by_last_name(last_name):
    with Session(engine) as session:
        query = select(User).filter_by(last_name = last_name)
        result = session.execute(query)
        return result.first()

def get_first_user():
    with Session(engine) as session:
        query = select(User)
        result = session.execute(query)
        return result.first()


def find_users():
    with Session(engine) as session:
        query = select(User)
        result = session.execute(query)
        print(result.all())


def create_center(name, address):
    with Session(engine) as session:
        center = FitnessCenter(
            center_name = name,
            center_address = address
        ) 
        session.add(center)
        session.commit()

def find_centers():
    with Session(engine) as session:
        query = select(FitnessCenter)
        result = session.execute(query)
        print(result.all())

def find_center_by_name(name):
    with Session(engine) as session:
        query = select(FitnessCenter)
        result = session.execute(query).first()
        return result[0]

def add_subscription(user: User, center: FitnessCenter):
    print(user)
    print(center)
    with Session(engine) as session:
        subscription = FitnessSubscription(
            user_id = user.user_id,
            center_id = center.center_id
        )
        session.add(subscription)
        session.commit()

def remove_subscription(subscription):
    pass

def get_subscriptions():
    with Session(engine) as session:
        stmt = \
            select(User, FitnessCenter).select_from(User) \
            .join(FitnessSubscription, User.user_id == FitnessSubscription.user_id) \
            .join(FitnessCenter, FitnessCenter.center_id == FitnessSubscription.center_id)
        print(stmt)
        return session.execute(stmt).all()

def add_schedule(user):
    pass

def remove_schedule(schedule):
    pass

def add_alarm(schedule, day_of_week, time_of_day):
    pass

def update_alarm(alarm, day_of_week, time_of_day):
    pass

def remove_alarm(alarm):
    pass


def add_profile(user, height, width):
    pass

def delete_profile(profile):
    pass

def get_profiles(user):
    pass

def show_stmts():
    print('\n\n'.join(str(stmt) for stmt in [
        select(User).join(User.subscriptions),
        select(User, FitnessSubscription).join(User.subscriptions),
        select(User.user_id, FitnessCenter.center_name).join(User.subscriptions, full=True),
        select(User.first_name, User.last_name, FitnessCenter.center_name).join(User.subscriptions).join(FitnessCenter.subscriptions)
    ]))