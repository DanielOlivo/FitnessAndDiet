from utils import *
from datetime import datetime, timedelta
from faker import Faker
import unittest
import re

fake = Faker()
fake.date_of_birth()
str(fake.date_of_birth())

datetime.strptime(str(fake.date_of_birth()), "%Y-%m-%d")

def create_alice_green():
    create_user('Alice', 'Green', date(1990, 10, 10), 'alice@mail.com', 'f')

def create_center1():
    create_center('center1', 'Haifa')



def handle_date(inputFn) -> datetime:
    while True:
        try:
            user_input = datetime.strptime(inputFn('Enter your date of birth'), "%Y-%m-%d")
            return user_input
        except:
            print('sorry, failed to parse the input, try again') 

def handle_gender(inputFn) -> str:
    while True:
        user_input = inputFn('Enter your gender. (F)emale or (M)ale: ').lower().strip()
        if user_input == 'm' or user_input == 'f':
            return user_input
        print('failed to parse, try again')

def handle_new_user(inputFn) -> User:
    first_name = inputFn(' Enter your first name: ') 
    last_name = inputFn('Enter your last name: ') 
    birth_date = handle_date(inputFn)
    email = inputFn('Enter your email address: ') 
    city = inputFn('Enter the city you live in: ') 
    gender = handle_gender(inputFn)
    create_user(first_name, last_name, birth_date, email, gender)

    user = get_user_by_fullname(first_name, last_name)
    return user

def handle_log_in(inputFn) -> User:
    print('Please present yourselves.')
    user_input = inputFn("Enter your first name and last name, separate by a space character: ")
    [first_name, last_name] = user_input.split(' ')
    if user_exists(first_name, last_name):
        return get_user_by_fullname(first_name, last_name)
    else:
        return handle_new_user(inputFn)

def handle_centers(user: User, inputFn) -> FitnessCenter:
    centers = get_user_centers(user)
    if centers: 
        return centers[0]

    user_fitness= inputFn('Do you have any subscription to a fitness center? (Y)es or (N)o: ').upper().strip()
    if user_fitness == 'Y':
        fitness_center_name = inputFn('Enter the name of the fitness center: ')
        if center_exists(fitness_center_name):
            return get_center_by_name(fitness_center_name) 
        else: 
            fitness_center_address = inputFn('Enter the address of the center: ')
            create_center(fitness_center_name, fitness_center_address)
            return get_center_by_name(fitness_center_name)
    else:
        print ('I am walking, running or swimming, by myself.')
        return None

def handle_new_alarms(schedule: Schedule, inputFn):
    while True: 
        print("Type Enter to start record the sessions of the week.")
        user_input = inputFn("<weekday> <hour>:<minutes> or type e(x)it to stop recording the schedule: ").lower().strip()

        if user_input == 'x':
            break

        result = re.search(r"^(\w+)\s+(\d\d):(\d\d)\s+(\d+)$", user_input) 

        if result:
            weekday = int(result.group(1))
            hour = int(result.group(2))
            minutes = int(result.group(3))
            duration = int(result.group(4))

            add_alarm(schedule, weekday, hour, minutes, duration)
        else:
            print("You haven\'t correctly typed the info. Try again.")


def handle_new_schedules(user: User, inputFn) -> Schedule:
    center = handle_centers(user, inputFn)
    add_schedule(user,center)
    schedule = get_schedules(user)[0]
    handle_new_alarms(schedule, inputFn)
    return schedule

def handle_profile_update(user: User, inputFn):
    height = float(inputFn('Enter your height in cm: '))
    weight = float(inputFn('Enter your weight in kg: '))
    add_profile(user,height, weight)
    

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
        self.assertEqual(center.center_name, center2[0].center_name)

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
            result = handle_date(lambda msg: str(self.fake.date_of_birth()))
            self.assertEqual(type(result), datetime)

