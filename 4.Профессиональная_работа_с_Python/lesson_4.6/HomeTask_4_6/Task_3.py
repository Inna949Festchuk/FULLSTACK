#Задача_3. Дан список поисковых источников.
#Получить количество (в %) слов вних.
#Например, поисковых источников из одного слова 5 %, из двух - 7 %, из трех - 3 % и т.д.

queries = [
  ' смотреть сериалы онлайн бесплатно через vpn сервер',
  'новости спорта олимпиады 2014 в СОЧИ',
  'афиша кино фантастика',
  'курс доллара',
  'сериалы этим летом',
  'курс по питону',
  'курс по питону самый крутой курс',
  ' ArcGIS ',
  'епрст '
  ]

in_queries = []
for querie in queries:
  end_space = querie.strip() #Удаление пробелов в начале и конце строки
  if querie != '':
    space = end_space.count(' ') + 1 #Подсчет входящих пробелов + 1 = количество слов
    in_queries.append(space)
max_in_queries = max(in_queries) #Определение максимального числа слов в поисковом запросе
for in_querie in range(max(in_queries)): #Подсчет вхождений числа слов
  count_in_querie = in_queries.count(max_in_queries)
  count_in_querie_percent = 100 / len(queries) * count_in_querie
  print (f'Запрос из {max_in_queries} слов(а) введен {count_in_querie} раз(а), что составляет {float(round(count_in_querie_percent, 1))} %')
  max_in_queries -= 1
