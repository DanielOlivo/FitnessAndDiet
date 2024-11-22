from utils import *
from datetime import datetime, timedelta
import unittest

class DbTest(unittest.TestCase):

    def test_all(self):
        create_database()

        now = datetime.now() - timedelta(minutes=5)

        '''There are two users'''
        create_user(
            first_name='Bob',
            last_name='Green',
            birth_date=date(1980, 10, 10),
            email = 'bob.green@gmail.com',
            gender='M'
        )

        create_user(
            first_name = 'Alice',
            last_name='Blue',
            birth_date=date(1990, 10, 10),
            email = 'alice.blue@gmail.com',
            gender='F'
        )

        users = find_users()
        self.assertEqual(len(users), 2, 'two users only')

        '''there are two fitness centers'''


        '''clean up after the test'''
        for (user, ) in get_users_after(now):
            delete_user(user)



    def test1(self):
        self.assertTrue(True)

    