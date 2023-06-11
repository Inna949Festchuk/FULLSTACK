import types
from itertools import chain


# _________________________
# task 1

class FlatIteratorV1:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.cursor_inner = -1
        self.cursor_outer = 0
        return self

    def __next__(self):
        self.cursor_inner += 1
        if self.cursor_inner >= len(self.list_of_list[self.cursor_outer]):
            self.cursor_outer += 1
            self.cursor_inner = 0
        if self.cursor_outer >= len(self.list_of_list):
            raise StopIteration
        return self.list_of_list[self.cursor_outer][self.cursor_inner]


class FlatIteratorV2:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.iterators = iter(iter(l) for l in self.list_of_list)
        self.current_iter = next(self.iterators)
        return self

    def __next__(self):
        try:
            next_item = next(self.current_iter)
        except StopIteration:
            self.current_iter = next(self.iterators)
            next_item = next(self.current_iter)
        return next_item


class FlatIteratorV3:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.flat_iter = chain.from_iterable(self.list_of_list)
        return self

    def __next__(self):
        return next(self.flat_iter)


class FlatIteratorV4:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        return chain.from_iterable(self.list_of_list)


# _________________________
# task 2

def flat_generator_v1(list_of_lists):
    for inner_list in list_of_lists:
        for item in inner_list:
            yield item


def flat_generator_v2(list_of_lists):
    for inner_list in list_of_lists:
        yield from inner_list


def flat_generator_v3(list_of_lists):
    for item in chain.from_iterable(list_of_lists):
        yield item


def flat_generator_v4(list_of_lists):
    return (item for item in chain.from_iterable(list_of_lists))

# _________________________
# task 3


class FlatIteratorHard:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.iters_stack = [iter(self.list_of_list)]
        return self

    def __next__(self):
        while self.iters_stack:
            try:
                next_item = next(self.iters_stack[-1])
                #  пытаемся получить следующий элемент
            except StopIteration:
                self.iters_stack.pop()
                #  если не получилось, значит итератор пустой
                continue

            if isinstance(next_item, list):
                # если следующий элемент оказался списком, то
                # добавляем его итератор в стек
                self.iters_stack.append(iter(next_item))

            else:
                return next_item
        raise StopIteration

# _________________________
# task 4


def flat_generator_v5(list_of_list):
    for i in list_of_list:
        if isinstance(i, list):
            for j in flat_generator_v5(i):
                yield j
        else:
            yield i


def test_task_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for IteratorClass in (FlatIteratorV1, FlatIteratorV2, FlatIteratorV3, FlatIteratorV4):

        for flat_iterator_item, check_item in zip(
                IteratorClass(list_of_lists_1),
                ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
        ):
            assert flat_iterator_item == check_item

        assert list(IteratorClass(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


def test_task_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for yield_function in (flat_generator_v1, flat_generator_v2, flat_generator_v3, flat_generator_v4):

        for flat_iterator_item, check_item in zip(
                yield_function(list_of_lists_1),
                ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
        ):
            assert flat_iterator_item == check_item

        assert list(yield_function(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

        assert isinstance(yield_function(list_of_lists_1), types.GeneratorType)


def test_task_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]
    for flat_iterator_item, check_item in zip(
            FlatIteratorHard(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIteratorHard(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


def test_task_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator_v5(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator_v5(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator_v5(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':

    test_task_1()
    test_task_2()
    test_task_3()
    test_task_4()