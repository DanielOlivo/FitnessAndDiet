from datetime import datetime
from models import *
from utils import *
import re
import requests

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



def get_past_and_incoming_alarm(alarms: list[Alarm]):
    dates = [(alarm,alarm.to_datetime()) for alarm in alarms]
    dates.sort(key=lambda x: x[1])
    (next_alarm, next_datetime) = dates[0]
    (prev_alarm, prev_datetime) = dates[-1]
    prev_datetime -= timedelta(days = 7)
    return ((prev_alarm, prev_datetime),(next_alarm, next_datetime))


def get_insult():
    try:
        response = requests.get("https://insult.mattbas.org/api/insult")
        return response.content
    except:
        return 'Failed to get response'


def get_training_notification(schedule: Schedule):
    alarms = get_alarms(schedule)
    ((past_alarm, past_datetime), (incoming_alarm, incoming_datetime)) = get_past_and_incoming_alarm(alarms)

    print(f'Your next training session is at {incoming_datetime},\nin {incoming_datetime - datetime.now()}') 
    print('\n\n')

    after_session_time = past_datetime + timedelta(hours=2) + timedelta(minutes=past_alarm.duration) 
    time_diff = datetime.now() - after_session_time

    if time_diff.days < 1:
        print('Have completed your training session, today?')
        confirmation_session = input('Enter (Y)es if it is done. Otherwse, (N)o: ').capitalize()
        if confirmation_session == 'Y':
            add_attendence(past_alarm,past_datetime, True)
            print("There is a part where we connect to some API with motivational quotes, but we ran out of time")
        else:
            add_attendence(past_alarm,past_datetime, False)
            #connect API with penalities injures
            api_response = get_insult()
            print("InsultAPI says: " + api_response)
            print("don't take it seriously - it is a joke")

    

