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

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[date]
    email: Mapped[str] = mapped_column(String(100))
    gender: Mapped[str] = mapped_column(String(1))

    subscriptions: Mapped[List['FitnessSubscription']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    schedules: Mapped[List['Schedule']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    profile: Mapped['Profile'] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'[User {self.user_id!r} {self.first_name!r} {self.last_name!r}]'


class FitnessCenter(Base):
    __tablename__ = 'fitness_center'

    center_id: Mapped[int] = mapped_column(primary_key=True)
    center_name: Mapped[str] = mapped_column(String(255))
    center_address: Mapped[str] = mapped_column(String(255))

    subscriptions: Mapped[List['FitnessSubscription']] = relationship(
        back_populates='center', cascade='all, delete-orphan'
    )
    schedules: Mapped[List['Schedule']] = relationship(
        back_populates='center', cascade='all, delete-orphan'
    )

class FitnessSubscription(Base):
    __tablename__ = 'fitness_subscription'

    subscription_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    center_id: Mapped[int] = mapped_column(ForeignKey('fitness_center.center_id'))

    user: Mapped['User'] = relationship(back_populates='subscriptions')
    center: Mapped['FitnessCenter'] = relationship(back_populates='subscriptions')

class Schedule(Base):
    __tablename__ = 'schedule'
    schedule_id: Mapped[int] = mapped_column(primary_key=True)
    center_id: Mapped[int]  = mapped_column(ForeignKey('fitness_center.center_id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))

    user: Mapped['User'] = relationship(back_populates='schedules')
    center: Mapped['FitnessCenter'] = relationship(back_populates='schedules')
    alarms: Mapped[List['Alarm']] = relationship(
        back_populates='schedule', cascade='all, delete-orphan'
    )

class Alarm(Base):
    __tablename__ = 'alarm'

    alarm_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    schedule_id: Mapped[int] = mapped_column(ForeignKey('schedule.schedule_id'), nullable=False)
    weekday: Mapped[int]  = mapped_column(nullable=False)
    hour: Mapped[int] = mapped_column(nullable=False)
    minutes: Mapped[int]  = mapped_column(nullable=False)
    duration: Mapped[int]

    schedule: Mapped['Schedule'] = relationship(back_populates='alarms')

class Profile(Base):
    __tablename__ = 'profile'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    height: Mapped[float] = mapped_column(nullable=False)
    update_date: Mapped[datetime] = mapped_column(nullable=False)
    notification: Mapped[datetime] = mapped_column(nullable=False)

    user: Mapped['User'] = relationship(back_populates='profile')