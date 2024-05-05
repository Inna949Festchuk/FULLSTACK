import csv
import itertools
import psycopg2
# # Для установки драйвера смени путь PATH=$PATH:/Applications/Postgres.app/Contents/Versions/12/bin/ pip install psycopg2

from tqdm import tqdm
from pprint import pprint

def iterated_cities():
    '''Функция-генератор, отдающая построчно значения функции insert_db()
    когда та запросит. Оператор yield призван не завершать выполнение
    функции после отдачи значения строки, как это делал бы return, а приостанавливать 
    ее выполнение и возобновлять при следующем запросе с места останова.
    Тем самым решается проблема утечки ОЗУ при работе с объемными файлами'''
	
    with open ("in_dataset/_cities.csv", "r", encoding = "utf-8") as in_data:
        in_cities = csv.reader(in_data, delimiter = ";")
        iter_list = itertools.islice(in_cities, 1, None) # Итерируем начиная с первой строки
        
        while True:
            
            try:
                
                new_list = next(iter_list) 
            
            except StopIteration:
                break
            
            yield new_list
        
def insert_db():
    '''Функция обработки запроса для заполнения таблицы базы данных'''
    
    conn = psycopg2.connect(database='Cities', user='postgres', password='Atoer949', host='localhost', port='5432')

    with conn.cursor() as cursor:
        
        try:
            
            for el in tqdm(iterated_cities()):
                if el[3] == '':
                    el[3] = int() # Так как поле el[3] в БД - integres, а в исходниках встречается '' (тип строка) 
                 
                cursor.execute("""INSERT INTO _cities VALUES (%s, %s, %s, %s, %s, %s,
                                                            %s, %s, %s, %s, %s, %s,
                                                            %s, %s, %s, %s, %s, %s,
                                                            %s, %s, %s, %s, %s, %s,
                                                            %s, %s, %s, %s, %s, %s,
                                                            %s, %s, %s, %s, %s, %s,
                                                            %s, %s, %s, %s, %s, %s,
                                                            %s, %s, %s, %s);""", el
                                                            )
                conn.commit()
                    
        except psycopg2.IntegrityError:
            print(":(")
            None

def select_db():
    '''Функция обработки запроса для выборки из таблиц базы данных и 
    сохранения результатов в .csv файл'''
    
    conn = psycopg2.connect(database='Cities', user='postgres', password='Atoer949', host='localhost', port='5432')

    with conn.cursor() as cursor:

        try:
        
            cursor.execute("""SELECT cit.city_id, cit.region_id, cit.country_id, cit.important, cit.title_ru, 
	                                cit.title_en, cit.region_ru, cit.region_en, cit.area_ru, cit.area_en, 
	                                con.country_id, con.title_ru, con.title_en 
                            FROM _cities AS cit
                            LEFT JOIN _countries AS con
                            ON cit.country_id = con.country_id;"""
                           )

            with open ("out_cities.csv", "w", encoding = "utf-8") as out_data:
                writer = csv.writer(out_data, delimiter=';', quoting=csv.QUOTE_ALL)
                writer.writerow(['city_id', 'region_id', 'country_id', 'important', 'title_ru', 
	                            'title_en', 'region_ru', 'region_en', 'area_ru', 'area_en', 
	                            'country_id', 'title_ru', 'title_en'
                                ])

                for row in tqdm(cursor.fetchall()):
                    writer.writerow(row)
                    
        except psycopg2.IntegrityError:
            print(":(")
            None

def main():
    insert_db()
    select_db()

if __name__ == '__main__':
    main()
