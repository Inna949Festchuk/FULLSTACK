from load_tag_m4a import meta_info_m4a
from insert_db import *

if __name__ == '__main__':
    import os
    
    # Чтение музыкальных файлв .m4a из дирректории dir в список
    dir = 'musicfile'
    filelist = list(filter(lambda i: '.m4a' in i, os.listdir(dir)))
    # print(filelist)
    
    # Заполнение атрибутов в БД
    for file_el in filelist:
        metadatas = meta_info_m4a(dir+'/'+file_el) # Чтение значений тегов из метаданных муз.файлов
        
        # Заполнение таблиц genre и performer
        insert_db_genre(metadatas.get('name_genre')) 
        insert_db_performer(metadatas.get('name_performer'))

        # Ручная Насстройка связей M:N (жанры:исполнители)
        # insert_db_genreperformer([1, 2, 2], [1, 2, 3])
        
        # Автоматизированное установление связей M:N (жанры:исполнители)
        genre_field = select_db_genreperformer('genre_id', 
                                            'genre', 
                                            'name_genre', 
                                            metadatas.get('name_genre')
                                            ) # Выборка id по по условию 
                                              # равенства тега муз.файла значению поля
        performer_field = select_db_genreperformer('performer_id', 
                                                'performer', 
                                                'name_performer', 
                                                metadatas.get('name_performer')
                                                )
        # Заполнение таблицы связей M:N
        insert_db_genreperformer(genre_field, performer_field )
        print(genre_field, performer_field)
        
        # Заполнение таблицs album
        insert_db_album(metadatas.get('name_album'), metadatas.get('date_album'))
        
        # Автоматизированное установление связей M:N (альбомы:исполнители)
        album_field = select_db_performeralbum('album_id', 
                                                'album', 
                                                'name_album',
                                                'date_album',
                                                metadatas.get('name_album'),
                                                metadatas.get('date_album')
                                                )
        # Заполнение таблицы связей M:N
        insert_db_performeralbum(album_field, performer_field)
        print(album_field, performer_field)

        # Заполнение таблицs album и установление связей 1:M (альбом:треки)
        insert_db_track(metadatas.get('name_track'), 
                        metadatas.get('duration_track'), 
                        album_field[0])


    