from utils import *
from datetime import datetime, timedelta
from faker import Faker
import unittest
import re
from interface_utils import *

fake = Faker()
fake.date_of_birth()
str(fake.date_of_birth())

datetime.strptime(str(fake.date_of_birth()), "%Y-%m-%d")

def create_alice_green():
    create_user('Alice', 'Green', date(1990, 10, 10), 'alice@mail.com', 'f')

def create_center1():
    create_center('center1', 'Haifa')

class FakeInput:
    def __init__(self, inputs):
        self.inputs = inputs
        self.idx = 0

    def __call__(self, *args, **kwds):
        if self.idx >= len(self.inputs):
            raise IndexError(f'no input for {args[0]}')
        self.idx += 1
        return self.inputs[self.idx - 1]  


class InterfaceTest(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.fake = Faker()

    def test_handle_profile_update(self):
        create_alice_green()
        user = get_user_by_fullname('Alice', 'Green')
        fake_input_fn = FakeInput([
            "180",
            "65",
            "181",
            "67",
            "182",
            "68"
        ]) 
        for _ in range(3):
            handle_profile_update(user, fake_input_fn)

        records = get_profiles(user)
        self.assertEqual(len(records), 3)
        delete_user(user)
    

    def test_handle_new_schedules(self):
        create_alice_green()
        user = get_user_by_fullname('Alice', 'Green')
        fake_input_fn = FakeInput([
            "y",
            "center1",
            "Haifa",
            "0 10:00 90",
            "x"
        ])
        schedule = handle_new_schedules(user, fake_input_fn)

        self.assertTrue(not schedule is None)

        delete_user(user)
        for center in get_centers():
            delete_center(center)

    def test_handle_new_alarms(self):
        create_alice_green()
        user = get_user_by_fullname('Alice', 'Green')
        add_schedule(user, None)
        schedule = get_schedules(user)[0]
        fake_input_fn = FakeInput([
            '0 10:00 90',
            '3 11:00 60',
            'x'
        ])
        handle_new_alarms(schedule, fake_input_fn)
        alarms = get_alarms(schedule)
        on_monday = [alarm for alarm in alarms if alarm.weekday == 0][0]
        on_thursday = [alarm for alarm in alarms if alarm.weekday == 3][0]

        self.assertEqual(on_monday.weekday, 0)
        self.assertEqual(on_monday.hour, 10)
        self.assertEqual(on_monday.duration, 90)
        self.assertEqual(on_thursday.weekday, 3)
        self.assertEqual(on_thursday.hour, 11)
        self.assertEqual(on_thursday.duration, 60)

        delete_user(user)

    def test_handle_centers_without_subscription(self):
        create_alice_green()
        user = get_user_by_fullname('Alice', 'Green')
        fake_input_fn = FakeInput([
            "y",
            'center1',
            'Haifa'
        ]) 
        center = handle_centers(user, fake_input_fn)
        self.assertEqual(center.center_address, 'Haifa')
        self.assertEqual(center.center_name, 'center1')
        delete_user(user)
        delete_center(center)

    def test_handle_centers_with_active_subscription(self):
        create_alice_green()
        create_center1()
        user = get_user_by_fullname('Alice', 'Green')
        center = get_center_by_name('center1')
        add_subscription(user, center)
        center2 = handle_centers(user, FakeInput([]))
        self.assertEqual(center.center_name, center2.center_name)

        delete_user(user)
        delete_center(center)

    def test_handle_log_in_with_unexisting_user(self):
        fake_input_fn = FakeInput([
            'Alice Green',
            'Alice', 'Green', 
            '1999-10-10', 
            'alice@mail.com', 
            'Haifa', 
            'f'
        ])
        user = handle_log_in(fake_input_fn)
        self.assertEqual(user.first_name, 'Alice')
        self.assertEqual(user.last_name, 'Green')
        delete_user(user)


    def test_handle_log_in_with_existing_user(self):
        create_user('Alice', 'Green', date(1990, 10, 10), 'alice@mail.com', 'f')
        fake_input_fn = FakeInput(['Alice Green'])
        user = handle_log_in(fake_input_fn)
        self.assertEqual(user.first_name, 'Alice')
        self.assertEqual(user.last_name, 'Green')
        delete_user(user)

    def test_handle_new_user(self):
        fake_input_fn = FakeInput(['Bob', 'Green', '1999-10-10', 'bob@mail.com', 'Haifa', 'm'])
        user = handle_new_user(fake_input_fn)

        self.assertEqual(user.first_name, 'Bob')
        delete_user(user)

    def test_handle_gender(self):
        self.assertEqual(handle_gender('m'), 'm')
        self.assertEqual(handle_gender('F'), 'f')


    def test_handle_date(self):
        for _ in range(10):
            result = handle_date(lambda _: str(self.fake.date_of_birth()))
            self.assertEqual(type(result), datetime)

