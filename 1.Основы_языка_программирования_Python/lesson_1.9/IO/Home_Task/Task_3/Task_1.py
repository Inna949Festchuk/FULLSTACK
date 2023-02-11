cook_book = {}
with open('cook_book.txt', 'rt', encoding = 'utf8') as file:
    for l in file:
        dish = l.strip() # Название блюда
        amount = file.readline() # Переключаемся на следующую строку. Это количество ингридиентов
        cook_book.update({dish: []}) # Задаем структуру словаря и обновляем словарь
        for i in range(int(amount)):
            ingredients = file.readline() # Перебор ингридиентов в строке
            ingredient, quantity, measure = ingredients.strip().split(' | ')
            cook_book[dish].append({'ingredient': ingredient, # Добавляем значения в список по ключу 'dish:'
                                     'quantity' : quantity,
                                     'measure' : measure})
        blank_line = file.readline() # Пропускаем пустую строку в исходном файле
print(file.name.rsplit('.', 1)[0] + ' =', cook_book, sep = '\n')