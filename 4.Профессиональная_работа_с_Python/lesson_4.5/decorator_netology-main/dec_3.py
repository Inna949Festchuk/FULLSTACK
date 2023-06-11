import requests


def cached(cache_size):
    def _cached(old_function):

        CACHE = {}

        def new_function(*args, **kwargs):

            key = f'{args}_{kwargs}'
            if key in CACHE:
                return CACHE[key]
            result = old_function(*args, **kwargs)
            if len(CACHE) >= cache_size:
                CACHE.popitem()
            CACHE[key] = result
            return result

        return new_function
    return _cached


@cached(cache_size=10)
def get_people(people_id):

    return requests.get(f'https://swapi.dev/api/people/{people_id}').json()
