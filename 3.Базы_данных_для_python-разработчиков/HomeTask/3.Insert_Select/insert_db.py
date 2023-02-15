import sqlalchemy

dbname = 'mydb'
user = 'demo_netology'
dbpass = 'pass'
host='localhost'
port = '5432'
db = f'postgresql://{user}:{dbpass}@{host}:{port}/{dbname}'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()


def insertArtists(artists):
	for artist in artists:
		try:
			connection.execute(f"""
				INSERT INTO Artists(name)    
				VALUES(\'{artist}\')
				;
				""")
		except sqlalchemy.exc.IntegrityError:
			print(f'WARNING. The artist \"{artist}\" not inserted. Already exists')


def insertStylesSong(styles):
	for style in styles:
		try:
			connection.execute(f"""
				INSERT INTO StylesSong(styleName)    
				VALUES(\'{style}\')
				;
				""")
		except sqlalchemy.exc.IntegrityError:
			print(f'WARNING. The style \"{style}\" not inserted. Already exists')


def insertAlbums(albums):
	for title, date in albums:
		connection.execute(f"""
			INSERT INTO Albums(title, year)    
			VALUES(\'{title}\',\'{date}\')
			;
			""")


def insertTracks(tracks):
	for album, track, duration in tracks:
		id_album, _ = connection.execute(f"""SELECT id, title FROM Albums
			WHERE title = \'{album}\'
			;""").fetchone()
		connection.execute(f"""
			INSERT INTO Tracks(idAlbum, name, timeDuration)    
			VALUES(\'{id_album}\',\'{track}\',\'{duration}\')
			;
			""")


def insertCollections(collections):
	for name, date in collections:
		connection.execute(f"""
			INSERT INTO Collections(name, year)    
			VALUES(\'{name}\',\'{date}\')
			;
			""")


def insertArtistsAlbums(artistsAlbums):
	for artist, album in artistsAlbums:
		id_album,_ = connection.execute(f"""SELECT id,title FROM Albums
			WHERE title = \'{album}\'
			;""").fetchone()
		id_artist,_ = connection.execute(f"""SELECT id,name FROM Artists
			WHERE name = \'{artist}\'
			;""").fetchone()
		connection.execute(f"""
			INSERT INTO ArtistsAlbums(idArtist, idAlbum)    
			VALUES(\'{id_artist}\',\'{id_album}\')
			;
			""")


def insertStylesArtists(stylesArtists):
	for artist, style in stylesArtists:
		id_style,_ = connection.execute(f"""SELECT id,styleName FROM StylesSong
			WHERE styleName = \'{style}\'
			;""").fetchone()
		id_artist,_ = connection.execute(f"""SELECT id,name FROM Artists
			WHERE name = \'{artist}\'
			;""").fetchone()
		connection.execute(f"""
			INSERT INTO StylesArtists(idArtist, idStyle)    
			VALUES(\'{id_artist}\',\'{id_style}\')
			;
			""")


def insertCollectionsSongs(collectionsSongs):
	for collection, track in collectionsSongs:
		id_collection,_ = connection.execute(f"""SELECT id,name FROM Collections
			WHERE name = \'{collection}\'
			;""").fetchone()
		id_track,_ = connection.execute(f"""SELECT id,name FROM Tracks
			WHERE name = \'{track}\'
			;""").fetchone()
		connection.execute(f"""
			INSERT INTO CollectionsSongs(idCollection, idTrack)    
			VALUES(\'{id_collection}\',\'{id_track}\')
			;
			""")


artists = ['fellow','the end', 'ho ho ho', 'best artist', 
'python songs', '123Art', 'has been hidden', 'new']
styles = ['pop', 'rock', 'rap', 'folk', 'downtempo', 'dnb']
albums = [
	('alb1','2019-02-01'),('alb2','2001-04-05'), # for artist 1
	('best friends','2021-08-14'),('rare','2018-01-31'), # for artist 2
	('my songs','2018-12-25'), # for artist 3
	('css','2020-11-14'), # for artist 4
	('lalala','2025-10-05'), # for artist 5
	('qwert','1980-01-08'), # for artist 6
	('asd','2018-05-07'), # for artist 7
	('zxc tgb','2019-01-01'), # for artist 8
]

# tracks = (album name, track name, duration)
tracks = [
	(albums[0][0],	'track1',		240), # for album 1
	(albums[0][0],	'track2',		125), 
	(albums[1][0],	'best song',	333), # for album 2
	(albums[1][0],	'my my my',		100),
	(albums[2][0],	'my track',		111), # for album 3
	(albums[3][0],	'css song',		123), # for album 4
	(albums[4][0],	'song',			50),  # for album 5
	(albums[5][0],	'qwert aaa',	159), # for album 6
	(albums[6][0],	'long',			591), # for album 7
	(albums[7][0],	'track123',		147), # for album 8
	(albums[8][0],	'track my',		354), # for album 9
	(albums[9][0],	'track my track',50), # for album 10
]
collections = [('coll1','2019-02-01'),('coll2','2001-04-05'), 
	('best collection','2021-08-14'),('temp','2018-01-31'),
	('my best songs','2018-12-25'), ('ttt','2000-11-14'), 
	('collect10','2025-10-05'), ('collect12','1980-01-08'), 
	('collect11','2018-05-07'), ('collect13','2019-01-01'), 
]
artistsAlbums = [
	(artists[0],albums[0][0]),
	(artists[1],albums[0][0]),
	(artists[2],albums[1][0]),
	(artists[3],albums[2][0]),
	(artists[4],albums[3][0]),
	(artists[5],albums[4][0]),
	(artists[6],albums[5][0]),
	(artists[7],albums[6][0]),
	(artists[7],albums[7][0]),
	(artists[7],albums[8][0]),
	(artists[2],albums[9][0]),
]
stylesArtists = [
	(artists[0],styles[0]),
	(artists[1],styles[0]),
	(artists[2],styles[1]),
	(artists[2],styles[5]),
	(artists[3],styles[2]),
	(artists[4],styles[3]),
	(artists[5],styles[4]),
	(artists[6],styles[5]),
	(artists[7],styles[4]),
	(artists[7],styles[3]),
	(artists[7],styles[2]),
]
collectionsSongs = [
	(collections[0][0], tracks[0][1]),
	(collections[0][0], tracks[1][1]),
	(collections[0][0], tracks[2][1]),

	(collections[1][0], tracks[0][1]),
	(collections[1][0], tracks[9][1]),

	(collections[2][0], tracks[2][1]),
	(collections[2][0], tracks[4][1]),
	(collections[2][0], tracks[5][1]),

	(collections[3][0], tracks[3][1]),
	(collections[3][0], tracks[6][1]),

	(collections[4][0], tracks[4][1]),
	(collections[4][0], tracks[5][1]),
	(collections[4][0], tracks[8][1]),

	(collections[5][0], tracks[9][1]),
	(collections[5][0], tracks[5][1]),

	(collections[6][0], tracks[6][1]),
	(collections[6][0], tracks[1][1]),
	(collections[6][0], tracks[0][1]),

	(collections[7][0], tracks[8][1]),
	(collections[7][0], tracks[1][1]),

	(collections[8][0], tracks[8][1]),
	(collections[8][0], tracks[0][1]),
	(collections[8][0], tracks[5][1]),

	(collections[9][0], tracks[9][1]),
	(collections[9][0], tracks[0][1]),
]

insertArtists(artists)
insertStylesSong(styles)
insertAlbums(albums)
insertTracks(tracks)
insertCollections(collections)
insertArtistsAlbums(artistsAlbums)
insertStylesArtists(stylesArtists)
insertCollectionsSongs(collectionsSongs)
