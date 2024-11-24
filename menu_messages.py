from utils import *
from datetime import datetime
import re
welcome_message= input(
    '''
    Welcome to the self motivated application. To measure your progress with weight and fitness session.
    It is totally free.
    We will ask you first your credentials. Together, we\'ll set the session(s).
    YOU MUST update on daily basis your accomplishment on the sessions, and your weight.
    ''')

def handle_new_user() -> User:
    user_first_name = input (' Enter your first name: ') 
    user_last_name = input ('Enter your last name: ') 
    user_dob = input ('Enter your date of birth. e.g. 2024-12-31: ') 
    dob = datetime.strptime(user_dob, "%Y-%m-%d")
    user_email = input ('Enter your email address: ') 
    user_city = input ('Enter the city you live in: ') 
    user_gender = input ('Enter your gender. (F)emale or (M)ale: ') 
    create_user(user_first_name, user_last_name, dob, user_email, user_city, user_gender)

    user = get_user_by_fullname(user_first_name, user_last_name)
    return user

def handle_log_in() -> User:
    print('Please present yourselves.')
    user_input = input("Enter your first name and last name, separate by a space character: ")
    [first_name, last_name] = user_input.split(' ')
    if user_exists(first_name, last_name):
        return get_user_by_fullname(first_name, last_name)
    else:
        return handle_new_user()

def handle_centers():
    user_fitness= input('Do you have any subscription to a fitness center? (Y)es or (N)o: ').upper().strip()
    if user_fitness == 'Y':
        fitness_center_name = input ('Enter the name of the fitness center: ')
        if center_exists(fitness_center_name):
            return get_center_by_name(fitness_center_name) 
        else: 
            fitness_center_address = input ('Enter the address of the center: ')
            create_center(fitness_center_name, fitness_center_address)
            return get_center_by_name(fitness_center_name)
    else:
        print ('I am walking, running or swimming, by myself.')
        return None

def handle_new_alarms(schedule: Schedule):
    while True: 
        print("Type Enter to start record the sessions of the week.")
        user_input = input("<weekday> <hour>:<minutes> or type e(x)it to stop recording the schedule: ").lower().strip()

        if user_input == 'x':
            break

        result = re.search(r"^(\w+)\s+(\d\d):(\d\d)\s+(\d+)$", user_input) 

        if result:
            weekday = int(result.group(1))
            hour = int(result.group(2))
            minutes = int(result.group(3))
            duration = int(result.group(4))

            add_alarm(schedule, weekday, hour, minutes, duration)
            break
        else:
            print("You haven\'t correctly typed the info. Try again.")


# #print the summary of the schedule
def handle_schedules(user: User) -> Schedule:
    schedule = get_schedules(user)
    if schedule:
        print(schedule)
        return schedule[0]
    else:
        add_schedule(user,None)
        schedule = get_schedules(user)[0]
        handle_new_alarms(schedule)
        return schedule

def get_past_and_incoming_alarm(alarms: list[Alarm]) -> Alarm:
    dates = [(alarm,alarm.to_datetime()) for alarm in alarms]
    dates.sort(key=lambda x: x[1])
    next_alarm = dates[0]
    previous_alarm = dates[-1]
    previous_alarm[1] -= timedelta(days = 7)
    return (previous_alarm,next_alarm)

def handle_commands(user: User):
    height = float(input ('Enter your height in cm: '))
    weight = float(input ('Enter your weight in kg: '))
    add_profile(user,height, weight)
    
def main():
    user = handle_log_in()
    schedule = handle_schedules(user)
    alarms = get_alarms(schedule)

    ((past_alarm, past_datetime), (incoming_alarm, incoming_datetime)) = get_past_and_incoming_alarm(alarms)
    print(f'Your next training session is at {incoming_datetime},\nin {incoming_datetime - datetime.now()}') 

    notification_time: datetime = past_datetime + timedelta(hours = 2, minutes =past_alarm.duration)
    time_difference = datetime.now() -notification_time

    if time_difference.days == 0:
        print('Have completed your training session, today?')
        confirmation_session = input('Enter (Y)es if it is done. Otherwse, (N)o: ').capitalize()
        if confirmation_session == 'Y':
            add_attendence(past_alarm,past_datetime, True)
            #connect API with reward GIF
        else:
            add_attendence(past_alarm,past_datetime, False)
            #connect API with penalities injures

    handle_commands(user)
    


