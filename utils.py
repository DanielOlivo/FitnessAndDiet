from typing import List
from sqlalchemy import String, Date, ForeignKey, Integer, URL, create_engine, select, func, and_, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from dotenv import load_dotenv
from datetime import date
from datetime import datetime

from models import *
import models
from engine import *

def create_database() -> None:
    models.Base.metadata.create_all(engine, checkfirst=True)

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
        return result.all()

def get_user_by_fullname(firstname, lastname) -> User:
    with Session(engine) as session:
        stmt = select(User).where(User.first_name == firstname and User.last_name == lastname)
        return session.execute(stmt).first()[0]

def get_users_after(datetime: datetime):
    with Session(engine) as session:
        stmt = select(User).where(User.creation_date >= datetime)
        return session.execute(stmt).all()

def delete_user(user: User):
    with Session(engine) as session:
        stmt = delete(User).where(User.user_id == user.user_id)
        session.execute(stmt)
        session.commit()


def create_center(name, address):
    with Session(engine) as session:
        center = FitnessCenter(
            center_name = name,
            center_address = address
        ) 
        session.add(center)
        session.commit()

def delete_center(center: FitnessCenter):
    with Session(engine) as session:
        stmt = delete(FitnessCenter).where(FitnessCenter.center_id == center.center_id)
        session.execute(stmt)
        session.commit()

def find_centers():
    with Session(engine) as session:
        query = select(FitnessCenter)
        return session.execute(query).all()

def find_centers_after(date: datetime):
    with Session(engine) as session:
        query = select(FitnessCenter).where(FitnessCenter.creation_date >= date)
        return session.execute(query).all()

def find_center_by_name(name) -> FitnessCenter:
    with Session(engine) as session:
        query = select(FitnessCenter)
        result = session.execute(query).first()
        return result[0]

def add_subscription(user: User, center: FitnessCenter):
    with Session(engine) as session:
        subscription = FitnessSubscription(
            user_id = user.user_id,
            center_id = center.center_id
        )
        session.add(subscription)
        session.commit()

def get_user_subscriptions(user: User) -> list[FitnessSubscription]:
    with Session(engine) as session:
        stmt = select(FitnessSubscription).where(FitnessSubscription.user_id == user.user_id)
        return session.execute(stmt).all()

def delete_subscription(subscription: FitnessSubscription):
    with Session(engine) as session:
        stmt = delete(FitnessSubscription).where(FitnessSubscription.subscription_id == subscription.subscription_id)
        session.execute(stmt)
        session.commit()

def get_subscriptions():
    with Session(engine) as session:
        stmt = \
            select(User, FitnessCenter).select_from(User) \
            .join(FitnessSubscription, User.user_id == FitnessSubscription.user_id) \
            .join(FitnessCenter, FitnessCenter.center_id == FitnessSubscription.center_id)
        print(stmt)
        return session.execute(stmt).all()

def get_subscriptions_after(date):
    with Session(engine) as session:
        stmt = select(FitnessSubscription).where(FitnessSubscription.creation_date >= date)
        return session.execute(stmt).all()



def add_schedule(user: User, center: FitnessCenter):
    with Session(engine) as session:
        schedule = Schedule(
            user_id = user.user_id,
            center_id = None if center is None else center.center_id
        )
        session.add(schedule)
        session.commit()

def remove_schedule(schedule: Schedule):
    with Session(engine) as session:
        session.delete(schedule)
        session.commit()

def get_schedules(user: User) -> list[Schedule]:
    with Session(engine) as session:
        query = select(Schedule).where(Schedule.user_id == user.user_id)
        return session.execute(query).all()

def get_alarms(schedule: Schedule):
    with Session(engine) as session:
        stmt = \
            select(Alarm) \
            .where(Alarm.schedule_id == schedule.schedule_id) \
            .order_by(Alarm.weekday.asc(), Alarm.hour.asc(), Alarm.minutes.asc())
        return session.execute(stmt).all()

def add_alarm(schedule: Schedule, day_of_week: int, hours: int, minutes: int, duration: int):
    with Session(engine) as session:
        alarm = Alarm(
            schedule_id = schedule.schedule_id,
            weekday = day_of_week,
            hour = hours,
            minutes = minutes,
            duration = duration
        )
        session.add(alarm)
        session.commit()

def update_alarm(alarm: Alarm, day_of_week=None, hours=None, minutes=None, duration=None):
    with Session(engine) as session:
        if not day_of_week is None:
            alarm.weekday = day_of_week
        if not hours is None:
            alarm.hour = hours 
        if not minutes is None:
            alarm.minutes = minutes
        if not duration is None:
            alarm.duration = duration
        session.add(alarm)
        session.commit()

def remove_alarm(alarm: Alarm):
    with Session(engine) as session:
        stmt = delete(Alarm).where(Alarm.alarm_id == alarm.alarm_id)
        session.execute(stmt)
        session.commit()

def add_profile(user: User, height: float, weight: float, notification: datetime):
    with Session(engine) as session:
        profile = Profile(
            user_id = user.user_id,
            weight = weight,
            height = height,
            notification = notification
        )
        session.add(profile)
        session.commit()

def get_last_profile(user: User):
    with Session(engine) as session:
        stmt = select(Profile).where(Profile.user_id == user.user_id).order_by(Profile.update_date.desc())
        return session.execute(stmt).first()

def delete_profile(profile: Profile):
    with Session(engine) as session:
        stmt = delete(Profile).where(Profile.id == profile.id)
        session.execute(stmt)
        session.commit()

def get_profiles(user: User):
    with Session(engine) as session:
        stmt = select(Profile).where(Profile.user_id == user.user_id)
        return session.execute(stmt).all()

def show_stmts():
    print('\n\n'.join(str(stmt) for stmt in [
        select(User).join(User.subscriptions),
        select(User, FitnessSubscription).join(User.subscriptions),
        select(User.user_id, FitnessCenter.center_name).join(User.subscriptions, full=True),
        select(User.first_name, User.last_name, FitnessCenter.center_name).join(User.subscriptions).join(FitnessCenter.subscriptions)
    ]))