# HomeTask-Modules-packages-imports-in-Python
Домашнее задание "Модули, пакеты, импорты в Python"
1. Разработать **структуру** программы "Бухгалтерия". 
- main.py;  
- application/salary.py;  
- application/db/people.py;    
main.py - основной модуль для запуска программы.  
В модуле salary.py функция calculate_salary.  
В модуле people.py функция get_employees.  

2. Импортировать функции в модуль main.py и вызывать эти функции в конструкции.
```
if __name__ == '__main__':
```
**Сами функции реализовать не надо**. Достаточно добавить туда какой-либо вывод.

3. Познакомиться с модулем [datetime](https://pythonworld.ru/moduli/modul-datetime.html). 
При вызове функций модуля main.py выводить текущую дату.

4. Найти интересный для себя пакет на [pypi](https://pypi.org/) и в файле requirements.txt указать его с актуальной версией. При желании можно написать программу с этим пакетом.
В рамках данного задания написана программа **[Схема движения по азимутам](https://github.com/Inna949Festchuk/Schema-Am)**, в которой применен пакет [matplotlib](https://pypi.org/project/matplotlib/), позволяющий построить график схемы в декартовой системе координат.
