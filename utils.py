from typing import List, Tuple
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

def create_user(first_name: str, last_name: str, birth_date: date, email: str, gender: str) -> None:
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

def get_user_by_last_name(last_name):
    with Session(engine) as session:
        query = select(User).filter_by(last_name = last_name)
        result = session.execute(query)
        return result.first()

def get_first_user():
    with Session(engine) as session:
        query = select(User)
        result = session.execute(query)
        return result.first()

def get_users() -> list[User]:
    '''returns all users'''
    with Session(engine) as session:
        query = select(User)
        result = session.execute(query)
        return [row[0] for row in result.all()]

def get_user_by_fullname(firstname: str, lastname: str) -> User:
    '''returns user with given full name'''
    with Session(engine) as session:
        stmt = select(User).where(User.first_name == firstname and User.last_name == lastname)
        return session.execute(stmt).first()[0]

def get_users_after(datetime: datetime) -> list[User]:
    '''returns all users which were created after datetime'''
    with Session(engine) as session:
        stmt = select(User).where(User.creation_date >= datetime)
        return [row[0] for row in session.execute(stmt).all()]

def delete_user(user: User) -> None:
    with Session(engine) as session:
        stmt = delete(User).where(User.user_id == user.user_id)
        session.execute(stmt)
        session.commit()


def create_center(name: str, address: str) -> None:
    with Session(engine) as session:
        center = FitnessCenter(
            center_name = name,
            center_address = address
        ) 
        session.add(center)
        session.commit()

def delete_center(center: FitnessCenter) -> None:
    with Session(engine) as session:
        stmt = delete(FitnessCenter).where(FitnessCenter.center_id == center.center_id)
        session.execute(stmt)
        session.commit()

def get_centers():
    '''returns all fitness centers'''
    with Session(engine) as session:
        query = select(FitnessCenter)
        return [row[0] for row in session.execute(query).all()]

def get_centers_after(date: datetime):
    with Session(engine) as session:
        query = select(FitnessCenter).where(FitnessCenter.creation_date >= date)
        return [row[0] for row in session.execute(query).all()]

def get_center_by_name(name: str) -> FitnessCenter:
    with Session(engine) as session:
        query = select(FitnessCenter).where(FitnessCenter.center_name == name)
        result = session.execute(query).first()
        return result[0]

def get_user_centers(user: User) -> list[FitnessCenter]:
    '''return all centers where given user have subscriptions'''
    with Session(engine) as session:
        query = select(FitnessCenter).join(FitnessCenter.subscriptions).where(FitnessSubscription.user_id == user.user_id)
        return [row[0] for row in session.execute(query).all()]

def add_subscription(user: User, center: FitnessCenter) -> None:
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
        stmt = select(User, FitnessCenter).join(User.subscriptions) #.join(FitnessCenter.subscriptions)
        return session.execute(stmt).all()

def get_subscriptions_after(date: datetime) -> list[FitnessSubscription]:
    with Session(engine) as session:
        stmt = select(FitnessSubscription).where(FitnessSubscription.creation_date >= date)
        return [row[0] for row in session.execute(stmt).all()]



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

def get_schedules(user: User) -> list[Tuple[Schedule]]:
    with Session(engine) as session:
        query = select(Schedule).where(Schedule.user_id == user.user_id)
        return session.execute(query).all()

def get_alarms(schedule: Schedule) -> list[Tuple[Alarm]]:
    with Session(engine) as session:
        stmt = \
            select(Alarm) \
            .where(Alarm.schedule_id == schedule.schedule_id) \
            .order_by(Alarm.weekday.asc(), Alarm.hour.asc(), Alarm.minutes.asc())
        return session.execute(stmt).all()

def get_alarms_after(date: datetime) -> list[Alarm]:
    with Session(engine) as session:
        query = select(Alarm).where(Alarm.creation_date >= date)
        return [row[0] for row in session.execute(query).all()]

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

def delete_alarm(alarm: Alarm):
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


def get_profiles_after(date: datetime) -> list[Profile]:
    with Session(engine) as session:
        stmt = select(Profile).where(Profile.update_date >= date)
        return [row[0] for row in session.execute(stmt).all()]



def show_stmts():
    print('\n\n'.join(str(stmt) for stmt in [
        select(User).join(User.subscriptions),
        select(User, FitnessSubscription).join(User.subscriptions),
        select(User.user_id, FitnessCenter.center_name).join(User.subscriptions, full=True),
        select(User.first_name, User.last_name, FitnessCenter.center_name).join(User.subscriptions).join(FitnessCenter.subscriptions)
    ]))