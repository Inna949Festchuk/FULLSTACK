# -*- coding: utf-8 -*-
# =============================================================================
"""Module insert data base."""
# File Name: insert_db.py
# =============================================================================

import psycopg2

# Insert
def insert_db(table, field, value):
    '''Функция обработки запроса для заполнения таблицы базы данных
    table - имя таблицы
    field - имя поля
    value - значения поля'''
    conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
    with conn.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO {table}({field}) VALUES('{value}');")
                conn.commit()
            except psycopg2.IntegrityError:
                print(f'Внимание! Найдено дублирующее значение.')

# # Insert
# def insert_db_genre(genre):
# 	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
# 	with conn.cursor() as cursor:
#             try:
#                 cursor.execute(f"INSERT INTO genre(name_genre) VALUES('{genre}');")
#                 conn.commit()
#             except psycopg2.IntegrityError:
#                 print('Внимание! Найдено дублирующее значение жанра.')

# # Insert
# def insert_db_performer(performer):
# 	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
# 	with conn.cursor() as cursor:
#             try:
#                 cursor.execute(f"INSERT INTO performer(name_performer) VALUES('{performer}');")
#                 conn.commit()
#             except psycopg2.IntegrityError:
#                 print('Внимание! Найдено дублирующее значение исполнителя.')


# Select From Where
def select_db_genreperformer(select_field, select_table, where_field, select_where):
    '''Функция выборки PK из таплицы по условию равенства тега муз.файла 
    значению поля для автоматизации формирования связей M:N'''
    conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
    with conn.cursor() as cursor:  
        try:
                cursor.execute(f"SELECT {select_field} FROM {select_table} WHERE {where_field} = '{select_where}'")
                for row in cursor:
                    return row
        except psycopg2.IntegrityError:
                print('Внимание! Связи уже установлены.')
            
# M:N
def insert_db_genreperformer(id_genre, id_performer):
    '''Функция заполнения таблицы связей M:N'''
    conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
    with conn.cursor() as cursor:
            try:
                for g, p in zip(id_genre, id_performer):
                    cursor.execute(f"INSERT INTO genreperformer(genre_field, performer_field) VALUES('{g}','{p}');")
                    conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Связи уже установлены.')

# Insert
def insert_db_album(album, date):
	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
	with conn.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO album(name_album, date_album) VALUES('{album}','{date}');")
                conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Найдено дублирующее значение альбома.')

# Select From Where
def select_db_performeralbum(select_field, select_table, where_field_1, where_field_2, select_where_1, select_where_2):
    '''Функция выборки PK из таплицы по условию равенства тега муз.файла 
    значению поля для автоматизации формирования связей M:N'''
    conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
    with conn.cursor() as cursor:  
        try:
                cursor.execute(f"SELECT {select_field} FROM {select_table} WHERE {where_field_1} = '{select_where_1}' AND {where_field_2} = '{select_where_2}'")
                for row in cursor:
                    return row
        except psycopg2.IntegrityError:
                print('Внимание! Связи уже установлены.')
            
# M:N
def insert_db_performeralbum(id_performer, id_album):
    '''Функция заполнения таблицы связей M:N'''
    conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
    with conn.cursor() as cursor:
            try:
                for g, p in zip(id_performer, id_album):
                    cursor.execute(f"INSERT INTO performeralbum(album_field, performer_field) VALUES('{g}','{p}');")
                    conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Связи уже установлены.')

# Insert
def insert_db_track(track, duration, album):
	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
	with conn.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO track(name_track, duration_track, album_field) VALUES('{track}','{duration}','{album}');")
                conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Найдено дублирующее значение трека.')

# Insert collection
def insert_db_collection(collection, date_coll):
	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
	with conn.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO collection(name_coll, date_coll) VALUES('{collection}','{date_coll}');")
                conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Найдено дублирующее значение сборников.')
            
# M:N collection
def insert_db_trackcollection(id_track, id_coll):
    '''Функция заполнения таблицы связей M:N'''
    conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
    with conn.cursor() as cursor:
            try:
                for g, p in zip(id_track, id_coll):
                    cursor.execute(f"INSERT INTO trackcollection(track_field, coll_field) VALUES('{g}','{p}');")
                    conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Связи уже установлены.')

# Delite dublicate
def delite_dubl_db():
	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
	with conn.cursor() as cursor:
            try:
                cursor.execute(f"DELETE from album a using album b where a.CTID < b.CTID and a.name_album = b.name_album and a.date_album = b.date_album;")
                cursor.execute(f"SELECT * FROM album;")
                conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Найдено дублирующее значение сборников.')
            
            