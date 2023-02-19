from load_tag_m4a import track_info_m4a
from insert_db import insert_db_genre, insert_db_performer, insert_db_album, insert_db_genreperformer

if __name__ == '__main__':
    import os
    
    # Чтение музыкальных файлв .m4a из дирректории dir в список
    dir = 'musicfile'
    filelist = list(filter(lambda i: '.m4a' in i, os.listdir(dir)))
    # print(filelist)
    
    # Заполнение атрибутов в БД
    for file_el in filelist:
        metadatas = track_info_m4a(dir+'/'+file_el) # Чтение значений атрибутов из метаданных файлов
        insert_db_genre(metadatas.get('name_genre'))
        insert_db_performer(metadatas.get('name_performer'))
        insert_db_album(metadatas.get('name_album'), metadatas.get('date_album'))
        print(metadatas)

    # Насстройка связи M:N (жанры:исполнители)
    insert_db_genreperformer([1, 2, 2], [1, 2, 3])
    