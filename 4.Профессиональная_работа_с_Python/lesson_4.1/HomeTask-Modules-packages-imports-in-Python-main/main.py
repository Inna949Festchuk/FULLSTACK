from datetime import datetime

from application.salary import calculate_salary as cs
from application.db.people import get_employees

if __name__ == '__main__':
    dt = datetime.today()
    print(dt)
    p = 'this is an imported definition calculate_salary()'
    cs(f'{p} {dt}')
    s = 'this is an imported get_employees()'
    get_employees(f'{s} {dt}')
