import requests
import datetime

from cachetools import cached


# @cached(max_size=50)
class People:

    def __init__(self, people_id, refresh=True):
        self.people_id = people_id
        if refresh:
            self.refresh()

    def refresh(self):
        self.data = requests.get(f'https://swapi.dev/api/people/{self.people_id}').json()

    @property
    def name(self):
        return self.data['name']

    @staticmethod
    def say_hi():
        print('HI')

    @classmethod
    def from_json(cls, json_data):
        people = cls(1, refresh=False)
        people.data = json_data
        return people


people = People.from_json({'name': 'Чубака'})
print(people.name)

people = People(1)
people.say_hi()
print(people.name)

people.refresh()