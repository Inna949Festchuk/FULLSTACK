from load_tag_m4a import track_info_m4a
from insert_db import insert_db_genre, insert_db_performer#, insert_db_album


if __name__ == '__main__':
    import os
    # Файлы в дирректории dir
    dir = 'musicfile'

    filelist = list(filter(lambda i: '.m4a' in i, os.listdir(dir)))
    print(filelist)
    
    for file_el in filelist:
        metadatas = track_info_m4a(dir+'/'+file_el)
        insert_db_genre(metadatas.get('name_genre'))
        insert_db_performer(metadatas.get('name_performer'))
        # insert_db_album(metadatas.get('name_album'), metadatas.get('date_album'))
        print(metadatas)

    