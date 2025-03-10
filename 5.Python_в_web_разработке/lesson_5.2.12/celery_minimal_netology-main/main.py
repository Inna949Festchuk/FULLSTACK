from tasks import cpu_bound_function


def main():

    async_result_1 = cpu_bound_function.delay(4, 1)
    async_result_2 = cpu_bound_function.delay(2, 21)
    async_result_3 = cpu_bound_function.delay(3, 3)
    async_result_4 = cpu_bound_function.delay(4, 4)

    result_1 = async_result_1.get()
    result_2 = async_result_2.get()
    result_3 = async_result_3.get()
    result_4 = async_result_4.get()

    print(result_1)
    print(result_2)
    print(result_3)
    print(result_4)


if __name__ == '__main__':
    main()