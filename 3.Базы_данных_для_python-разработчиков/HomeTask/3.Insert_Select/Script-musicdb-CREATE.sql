-- Сущность Жанр
CREATE TABLE IF NOT EXISTS Genre(
	genre_id serial PRIMARY	KEY,
	name_genre varchar(500) NOT NULL UNIQUE -- Уникальность значений
);

-- Пробуем добавить строку Жанр 
--insert into Genre(name_genre) values('three Genre')

-- Сущность Исполнитель
CREATE TABLE IF NOT EXISTS Performer(
	performer_id serial PRIMARY KEY,
	name_performer varchar(500) NOT NULL UNIQUE -- Уникальность значений
);

-- Пробуем добавить строку Performer 
--insert into Performer(name_performer) values('two Performer')

-- Кординальность N:M
-- Исполнители могут петь в разных жанрах, 
-- Как и одному жанру могут принадлежать несколько исполнителей
CREATE TABLE IF NOT EXISTS GenrePerformer(
	genre_field integer REFERENCES Genre(genre_id),
	performer_field integer REFERENCES Performer(performer_id),
	constraint pk PRIMARY KEY (genre_field, performer_field)
);

-- Пробуем связать Жанры и Исполнителей N:M
--insert into GenrePerformer(genre_field, performer_field) values(3, 2)

-- Сущность Альбом
CREATE TABLE IF NOT EXISTS Album(
	album_id serial PRIMARY KEY,
	name_album varchar(500) NOT NULL,
	-- date_album date NOT NULL CHECK(date_album > make_date(2000, 1, 1)) -- Ограничение даты альбома
	date_album date NOT NULL,
	UNIQUE (name_album, date_album) -- Уникальность в обоих полях
);

-- Пробуем добавить строку в Альбом 
--insert into Album(name_album, date_album) values('one Album', '2000-1-2')

-- Кординальность N:M
-- Альбом могут выпустить несколько исполнителей вместе, 
-- Как и исполнитель может принимать участие во множестве альбомов
CREATE TABLE IF NOT EXISTS PerformerAlbum(
	album_field integer REFERENCES Album(album_id),
	performer_field integer REFERENCES Performer(performer_id),
	constraint pk2 PRIMARY KEY (album_field, performer_field)
);

-- Сущность Трек. Кординальность 1:M. Трек принадлежит строго одному альбому
CREATE TABLE IF NOT EXISTS Track(
	track_id serial PRIMARY KEY,
	name_track varchar(500) NOT NULL,
	duration_track time NOT NULL,
	album_field integer NOT NULL REFERENCES Album(album_id)
);

-- Сущность Сборник
CREATE TABLE IF NOT EXISTS Collection(
	coll_id serial PRIMARY KEY,
	name_coll varchar(500) NOT NULL,
	date_coll date NOT NULL,
	UNIQUE (name_coll, date_coll) -- Уникальность в обоих полях
);

-- Кординальность N:M
-- В Сборник входят различные Треки из разных Альбомов.
CREATE TABLE IF NOT EXISTS TrackCollection(
	track_field integer REFERENCES Track(track_id),
	coll_field integer REFERENCES Collection(coll_id),
	constraint pk3 PRIMARY KEY (track_field, coll_field)
);
 
-- DELETE from album a using album b where a.CTID < b.CTID and a.name_album = b.name_album and a.date_album = b.date_album;