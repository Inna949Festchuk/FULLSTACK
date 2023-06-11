from functools import wraps


def cached(max_size):
    
    number_of_calls_with_this_size = 0
    
    def _cached(old_function):

        cache = {}
        number_of_calls = 0

        @wraps(old_function)
        def new_function(*args, **kwargs):
            key = f'{args}_{kwargs}'
            nonlocal number_of_calls, number_of_calls_with_this_size
            number_of_calls_with_this_size += 1

            number_of_calls += 1
            if key in cache:
                return cache[key]

            if len(cache) >= max_size:
                cache.popitem()

            result = old_function(*args, **kwargs)
            cache[key] = result
            return result

        return new_function
    return _cached