from tinytag import TinyTag

def track_info_m4a(filename):
    tag = TinyTag.get(filename)
    """Module Built To Read M4A Track Data."""
    print(tag.album)         # album as string
    print(tag.albumartist)   # album artist as string
    print(tag.artist)        # artist name as string
    print(tag.audio_offset)  # number of bytes before audio data begins
    # print(tag.bitdepth)      # bit depth for lossless audio
    print(tag.bitrate)       # bitrate in kBits/s
    print(tag.comment)       # file comment as string
    print(tag.composer)      # composer as string 
    print(tag.disc)          # disc number
    print(tag.disc_total)    # the total number of discs
    print(duration_from_seconds(tag.duration))      # duration of the song in seconds
    print(tag.filesize)      # file size in bytes
    print(tag.genre)         # genre as string
    print(tag.samplerate)    # samples per second
    print(tag.title)         # title of the song
    print(tag.track)         # track number as string
    print(tag.track_total)   # total number of tracks as string
    print(tag.year)          # year or date as string


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

if __name__ == '__main__':
    import os
    # Файлы в дирректории dir
    dir = 'mp3'
    filelist = os.listdir(dir)
    print(filelist)

    track_info_m4a(dir+'/01 Группа Крови.m4a')