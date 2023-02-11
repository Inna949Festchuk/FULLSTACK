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

def get_shop_list_by_dishes(dishes, person_count):
  dish_lists = []
  for el_dish_lists in dishes:
    dish_lists.append(el_dish_lists) # Список блюд
  dish_dict = {} # Словарь раскладки продуктов
  for dish_list in dish_lists: # Перебор по списку блюд
    for ingredient_list in cook_book[dish_list]: # Перебор по списку раскладки
      if ingredient_list['ingredient'] in list(dish_dict.keys()): # Контроль дублирования ингридиентов
        print('Продублирована раскладка для повторяющегося ингридиента:', ingredient_list['ingredient'])
        # Складываем количество повторяющихся ингридиентов в предшевствующем и настоящем списках dish_dict
        dish_dict[ingredient_list['ingredient']] = {'measure': ingredient_list['measure'], 
                                                    'quantity': int(ingredient_list['quantity']) * person_count 
                                                    + int(dish_dict[ingredient_list['ingredient']]['quantity'])} 
      else:
        dish_dict.update({ingredient_list['ingredient']: {'measure': ingredient_list['measure'], 
                          'quantity': int(ingredient_list['quantity']) * person_count}}) 
  return dish_dict

res = get_shop_list_by_dishes(['Омлет', 'Фахитос', 'Утка по-пекински', 'Запеченый картофель'], 2)
print(res)
