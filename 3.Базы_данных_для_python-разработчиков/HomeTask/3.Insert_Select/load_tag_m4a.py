from tinytag import TinyTag
import psycopg2

def track_info_m4a(filename):
    tag = TinyTag.get(filename)
    """Module Built To Read M4A Track Data."""
    # print(tag.album)         # album as string
    # print(tag.albumartist)   # album artist as string
    # print(tag.artist)        # artist name as string
    # print(tag.audio_offset)  # number of bytes before audio data begins
    # # print(tag.bitdepth)      # bit depth for lossless audio
    # print(tag.bitrate)       # bitrate in kBits/s
    # print(tag.comment)       # file comment as string
    # print(tag.composer)      # composer as string 
    # print(tag.disc)          # disc number
    # print(tag.disc_total)    # the total number of discs
    # print(duration_from_seconds(tag.duration))      # duration of the song in seconds
    # print(tag.filesize)      # file size in bytes
    # print(tag.genre)         # genre as string
    # print(tag.samplerate)    # samples per second
    # print(tag.title)         # title of the song
    # print(tag.track)         # track number as string
    # print(tag.track_total)   # total number of tracks as string
    # print(tag.year)          # year or date as string

    name_genre = tag.genre # Жанр
    name_performer = tag.composer  # Исполнитель
    name_album = tag.album # Альбом
    date_album = tag.year # Дата альбома
    name_track = tag.track_total # Трэк
    duration_track = duration_from_seconds(tag.duration) # Продолжительность трэка
    
    metalist = {'name_genre':name_genre, 'name_performer':name_performer, 'name_album':name_album,
                'date_album':date_album, 'name_track':name_track, 'duration_track':duration_track}
    return metalist

def duration_from_seconds(s):
    """Module to get the convert Seconds to a time like format."""
    s = s
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    timelapsed = "{:01d}:{:02d}:{:02d}:{:02d}".format(int(d),
                                                      int(h),
                                                      int(m),
                                                      int(s))
    return timelapsed

def insert_db(genre):
	conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')
	with conn.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO genre(name_genre) VALUES('{genre.get('name_genre')}');")
                conn.commit()
            except psycopg2.IntegrityError:
                print('Внимание! Найдено дублирующее значение жанра.')

if __name__ == '__main__':
    import os
    # Файлы в дирректории dir
    dir = 'musicfile'

    filelist = list(filter(lambda i: '.m4a' in i, os.listdir(dir)))
    print(filelist)
    
    for file_el in filelist:
        metadatas = track_info_m4a(dir+'/'+file_el)
        insert_db(metadatas)
        print(metadatas)