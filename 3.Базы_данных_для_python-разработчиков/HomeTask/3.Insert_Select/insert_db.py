# -*- coding: utf-8 -*-
# =============================================================================
"""Module insert data base."""
# File Name: insert_db.py
# =============================================================================

import psycopg2

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
# M:N
def insert_db_genreperformer(id_genre, id_performer):
	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
	with conn.cursor() as cursor:
            try:
                for g, p in zip(id_genre, id_performer):
                    cursor.execute(f"INSERT INTO genreperformer(genre_field, performer_field) VALUES('{g}','{p}');")
                    conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Связи установлены.')

def insert_db_album(album, date):
	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
	with conn.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO album(name_album, date_album) VALUES('{album}','{date}');")
                conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Год издания < 2000.')