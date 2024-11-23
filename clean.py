from utils import *
from datetime import datetime, timedelta
import sys

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('resetting the whole db...')
        drop_database()
        create_database()
        print("...done")
    elif '-m' in sys.argv:
        minutes = int(sys.argv[2])
        print(f'removing everything starting {minutes} minutes ago')
        date = datetime.now() - timedelta(minutes=minutes)

    else:
        print("don't get it")
