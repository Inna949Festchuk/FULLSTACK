import requests
import datetime

from cachetools import cached


@cached(cache={})
def get_people(people_id):

    return requests.get(f'https://swapi.dev/api/people/{people_id}').json()

start = datetime.datetime.now()
print(get_people(1))
end = datetime.datetime.now()
print(end - start)

start = datetime.datetime.now()
print(get_people(1))
end = datetime.datetime.now()
print(end - start)