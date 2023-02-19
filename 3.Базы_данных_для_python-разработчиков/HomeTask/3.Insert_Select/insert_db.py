# -*- coding: utf-8 -*-
# =============================================================================
"""Module insert data base."""
# File Name: insert_db.py
# =============================================================================

import psycopg2

conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
def insert_db_genre(genre):
	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
	with conn.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO genre(name_genre) VALUES('{genre}');")
                conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Найдено дублирующее значение жанра.')

def insert_db_performer(performer):
	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
	with conn.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO performer(name_performer) VALUES('{performer}');")
                conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Найдено дублирующее значение исполнителя.')

# def insert_db_album(album, date):
# 	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
# 	with conn.cursor() as cursor:
#             try:
#                 cursor.execute(f"INSERT INTO performer(name_performer) VALUES('{album}');")
#                 cursor.execute(f"INSERT INTO performer(date_album) VALUES('{date}');")
#                 conn.commit()
#             except psycopg2.IntegrityError:
#                 print('Внимание! Найдено дублирующее значение исполнителя.')