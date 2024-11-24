from datetime import datetime
import re
from interface_utils import *
from utils import *

welcome_message= '''
    Welcome to the self motivated application. To measure your progress with weight and fitness session.
    It is totally free.
    We will ask you first your credentials. Together, we\'ll set the session(s).
    YOU MUST update on daily basis your accomplishment on the sessions, and your weight.
    '''

    
def main(inputFn):
    print(welcome_message)

    user = handle_log_in(inputFn)
    schedules = get_schedules(user)

    schedule = None
    if not schedules:
        schedule = handle_new_schedules(user, inputFn)
    else:
        schedule = schedules[0]

    alarms = get_alarms(schedule)
    if alarms:
        print(get_training_notification(schedule))

    print("Let's add new record")
    handle_profile_update(user, inputFn)

    get_training_notification(schedule)

    print("That's all, buy!")


if __name__ == '__main__':
    main(input)
