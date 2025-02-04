import datetime

import requests


def get_people(person_id):
    return requests.get(f"https://swapi.py4e.com/api/people/{person_id}/").json()


def main():
    response_1 = get_people(1)
    response_2 = get_people(2)
    response_3 = get_people(3)
    response_4 = get_people(4)
    print(response_1, response_2, response_3, response_4)


start = datetime.datetime.now()
main()
print(datetime.datetime.now() - start)
