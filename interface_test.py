from utils import *
from datetime import datetime, timedelta
from faker import Faker
import unittest

fake = Faker()
fake.date_of_birth()
str(fake.date_of_birth())

datetime.strptime(str(fake.date_of_birth()), "%Y-%m-%d")

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

def handle_centers():
    pass

class FakeInput:
    def __init__(self, inputs):
        self.inputs = inputs
        self.idx = 0

    def __call__(self, *args, **kwds):
        self.idx += 1
        return self.inputs[self.idx - 1]  


class InterfaceTest(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.fake = Faker()

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

