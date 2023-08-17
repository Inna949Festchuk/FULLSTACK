import os
import datetime
import time


def time_view():
    cur_data = datetime.date.isoformat(datetime.date.today())
    cur_time = time.strftime('%A %I:%M:%S %p')
    return cur_data, cur_time

def workdir_view():
    my_workdir = os.getcwd()
    return my_workdir

if __name__ == '__main__':
    print(f'рабочая дирректория: {workdir_view()}')
    print(f'дата и время: {time_view()}')
