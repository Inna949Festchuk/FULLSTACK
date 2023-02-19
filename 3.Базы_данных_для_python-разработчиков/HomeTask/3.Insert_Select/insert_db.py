# -*- coding: utf-8 -*-
# =============================================================================
"""Module insert data base."""
# File Name: insert_db.py
# =============================================================================

import psycopg2

def insert_db(genre):
	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
	with conn.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO genre(name_genre) VALUES('{genre.get('name_genre')}');")
                conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Найдено дублирующее значение жанра.')