from utils import *
from datetime import datetime, timedelta
import unittest

class DbTest(unittest.TestCase):

    @staticmethod
    def clean(date):
        for (user, ) in get_users_after(date):
            delete_user(user)

        for (center, ) in find_centers_after(date):
            delete_center(center)

        # for (subscription, ) in get_subscriptions_after(date):
        #     delete_subscription(subscription)


    def test_all(self):
        create_database()

        now = datetime.now() - timedelta(minutes=5)

        '''clean up before the test'''
        DbTest.clean(now)



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
        create_center(
            name = 'center 1',
            address = 'Haifa'
        )
        create_center(
            name = 'center 2',
            address = 'Tel Aviv'
        )
        centers = find_centers()
        self.assertEqual(len(centers), 2, 'two centers only')


        '''Bob has a subscription in center 1'''
        bob = get_user_by_fullname('Bob', 'Green')
        self.assertEqual(bob.first_name, 'Bob')
        self.assertEqual(bob.last_name, 'Green')

        center1 = find_center_by_name('center 1')
        self.assertEqual(center1.center_name, 'center 1')


        add_subscription(bob, center1)
        bobs_subscriptions = get_user_subscriptions(bob)
        self.assertEqual(len(bobs_subscriptions), 1)

        '''Bob has a schedule''' 
        add_schedule(bob, center1) 
        bobs_schedules = get_schedules(bob)
        self.assertEqual(len(bobs_schedules), 1)


        '''clean up after the test'''
        DbTest.clean(now)


    def test1(self):
        self.assertTrue(True)

    