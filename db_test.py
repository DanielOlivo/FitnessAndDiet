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
        bobs_schedule = bobs_schedules[0][0]


        '''Bob worksout one time per week'''
        add_alarm(bobs_schedule, 1, 18, 0, 90)
        bobs_alarms = get_alarms(bobs_schedule)
        first_alarm = bobs_alarms[0][0]

        self.assertEqual(len(bobs_alarms), 1)
        self.assertEqual(type(first_alarm), Alarm)
        self.assertEqual(first_alarm.weekday, 1)


        '''Bob decided to change the day for workout - to Wedndesday'''
        update_alarm(first_alarm, day_of_week=4) 
        first_alarm = get_alarms(bobs_schedule)[0][0]
        self.assertEqual(first_alarm.weekday, 4)


        '''Bob updates his wieght'''
        add_profile(bob, 180, 65, now + timedelta(days=1))

        '''he gained 5kg more'''
        add_profile(bob, 180, 70, now + timedelta(days=1))


        bob_profile_records = [row[0] for row in get_profiles(bob)]
        self.assertEqual(len(bob_profile_records), 2)
        self.assertEqual(type(bob_profile_records[0]), Profile)


        '''Alice doesn't need any fitness center - she works out by herself (center is None)'''
        alice = get_user_by_fullname('Alice', 'Blue')
        add_schedule(alice, center = None)
        alices_schedules = get_schedules(alice)

        self.assertEqual(len(alices_schedules), 1)
        alice_schedule = alices_schedules[0][0]
        self.assertEqual(type(alice_schedule), Schedule)
        
        self.assertTrue(alice_schedule.center_id is None)

        '''clean up after the test'''
        DbTest.clean(now)


    def test1(self):
        self.assertTrue(True)

    