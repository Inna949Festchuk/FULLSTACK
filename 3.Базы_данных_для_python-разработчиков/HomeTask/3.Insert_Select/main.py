from load_tag_m4a import meta_info_m4a
from processing_request import *

if __name__ == '__main__':
    import os
    from tqdm import tqdm
    
    # Чтение музыкальных файлв .m4a из дирректории dir в список
    dir = 'musicfile'
    filelist = list(filter(lambda i: '.m4a' in i, os.listdir(dir)))
    # print(filelist)
    
    # Заполнение атрибутов в БД
    for file_el in tqdm(filelist):
        metadatas = meta_info_m4a(dir+'/'+file_el) # Чтение значений тегов из метаданных муз.файлов
        
        # Заполнение таблиц genre и performer
        insert_db('performer', 'name_performer', metadatas.get('name_performer'))
        insert_db('genre', 'name_genre', metadatas.get('name_genre'))
        
        # Ручная Насстройка связей M:N (жанры:исполнители)
        # insert_db_genreperformer([1, 2, 2], [1, 2, 3])
        
        # Автоматизированное установление связей M:N (жанры:исполнители)
        # Выборка id по по условию равенства тега муз.файла значению поля
        PK_genre_field = select_db('genre_id', 'genre', 'name_genre', metadatas.get('name_genre'))
        PK_performer_field = select_db('performer_id', 'performer', 'name_performer', metadatas.get('name_performer'))

        # Заполнение таблицы связей M:N genreperformer
        insert_db_M_N('genreperformer', 'genre_field', 'performer_field', PK_genre_field, PK_performer_field)
        
         # Заполнение таблицы album
        insert_db('album', 'name_album', metadatas.get('name_album'), 'date_album', metadatas.get('date_album'))

        # Автоматизированное установление связей M:N (альбомы:исполнители)
        PK_album_field = select_db('album_id', 'album', 'name_album', metadatas.get('name_album'), 'date_album', metadatas.get('date_album'))
        PK_performer_field = select_db('performer_id', 'performer', 'name_performer', metadatas.get('name_performer'))
      
        # Заполнение таблицы связей M:N performeralbum
        insert_db_M_N('performeralbum', 'album_field', 'performer_field', PK_album_field, PK_performer_field)

        # Заполнение таблицs album и установление связей 1:M (альбом:треки)
        insert_db('track', 'name_track', metadatas.get('name_track'), 'duration_track', metadatas.get('duration_track'), 'album_field', PK_album_field[0])
        
        # Заполнение таблицы collection
        if metadatas.get('name_artist') == 'Разные артисты':
            insert_db('collection', 'name_coll', metadatas.get('name_album'), 'date_coll', metadatas.get('date_album'))
            PK_track_field = select_db('track_id', 'track', 'name_track', metadatas.get('name_track'))
            PK_coll_field = select_db('coll_id', 'collection', 'name_coll', metadatas.get('name_album'), 'date_coll', metadatas.get('date_album'))
            insert_db_M_N('trackcollection', 'track_field', 'coll_field', PK_track_field, PK_coll_field)
    

    