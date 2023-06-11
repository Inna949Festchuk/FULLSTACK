# -*- coding: utf-8 -*-
"""Module insert data base"""
# File Name: processing_request.py

import psycopg2
# Для установки драйвера смени путь PATH=$PATH:/Applications/Postgres.app/Contents/Versions/12/bin/ pip install psycopg2

# Insert
def insert_db(table, field_1, value_1, field_2=None, value_2=None, field_3=None, value_3=None):
    '''Функция обработки запроса для заполнения таблицы базы данных
    table - имя таблицы
    field - имя поля
    value - значения поля'''
    conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
    with conn.cursor() as cursor:
            try:
                if field_2 == None and value_2 == None and field_3 == None and value_3 == None:
                    cursor.execute(f"INSERT INTO {table}({field_1}) VALUES('{value_1}');")
                    conn.commit()
                elif field_3 == None and value_3 == None:
                    cursor.execute(f"INSERT INTO {table}({field_1}, {field_2}) VALUES('{value_1}', '{value_2}');")
                    conn.commit()
                else:
                    cursor.execute(f"INSERT INTO {table}({field_1}, {field_2}, {field_3}) VALUES('{value_1}', '{value_2}', '{value_3}');")
                    conn.commit()                     
            except psycopg2.IntegrityError:
                None
                # print(f'Внимание! Найдено дублирующее значение.')

# Select From Where
def select_db(select_field, select_table, where_field_1, select_where_1, where_field_2=None, select_where_2=None):
    '''Функция выборки PK из таплицы по условию равенства тега муз.файла 
    значению поля для автоматизации формирования связей M:N'''
    conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
    with conn.cursor() as cursor:  
        try:
            if where_field_2 == None and select_where_2 == None:
                cursor.execute(f"SELECT {select_field} FROM {select_table} WHERE {where_field_1} = '{select_where_1}'")
                for row in cursor:
                    return row
            else:                
                cursor.execute(f"SELECT {select_field} FROM {select_table} WHERE {where_field_1} = '{select_where_1}' AND {where_field_2} = '{select_where_2}'")
                for row in cursor:
                    return row
        except psycopg2.IntegrityError:
            None
            # print('Внимание! Связи уже установлены.')

# M:N
def insert_db_M_N(table, FK_M, FK_N, PK_M:list, PK_N:list):
    '''Функция заполнения таблицы связей M:N'''
    conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
    with conn.cursor() as cursor:
            try:
                for m, n in zip(PK_M, PK_N):
                    cursor.execute(f"INSERT INTO {table}({FK_M}, {FK_N}) VALUES('{m}','{n}');")
                    conn.commit()
            except psycopg2.IntegrityError:
                None
                # print('Внимание! Связи уже установлены.')


            
            