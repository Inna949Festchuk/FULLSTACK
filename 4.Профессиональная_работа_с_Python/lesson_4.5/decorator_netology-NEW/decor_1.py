def cached(old_function):

    cache = {}

    def new_function(*args, **kwargs):
        key = f'{args}_{kwargs}'

        if key in cache:
            return cache[key]
        result = old_function(*args, **kwargs)
        cache[key] = result
        return result

    return new_function