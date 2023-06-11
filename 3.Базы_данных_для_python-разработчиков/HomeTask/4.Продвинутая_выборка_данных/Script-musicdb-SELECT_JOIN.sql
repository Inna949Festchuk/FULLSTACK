-- 1. Количество исполнителей в каждом жанре
SELECT genre.name_genre, count(genreperformer.performer_field) AS count_performer FROM genre
INNER JOIN genreperformer ON genre.genre_id = genreperformer.genre_field
GROUP BY genre.genre_id;

-- 2. Количество треков вошедших в альбомы 2019-2020 годов (1987-1992 годов включительно)
-- SELECT album.name_album, album.date_album, count(track.track_id) AS count_track FROM album
-- INNER JOIN track ON album.album_id = track.album_field 
-- WHERE album.date_album BETWEEN make_date(1987, 1, 1) AND make_date(1992, 12, 31)
-- GROUP BY album.album_id;

-- 2. ИСПРАВЛЕННЫЙ ВАРИАНТ. Количество треков вошедших в альбомы 2019-2020 годов (1987-1992 годов включительно)
SELECT count(track.track_id) AS count_track FROM album
INNER JOIN track ON album.album_id = track.album_field
WHERE album.date_album BETWEEN make_date(1987, 1, 1) AND make_date(1992, 12, 31);

-- 3. Средняя продолжительность треков по каждому альбому
SELECT album.name_album, album.date_album, AVG(track.duration_track) AS average_track_length FROM album
INNER JOIN track ON album.album_id = track.album_field 
GROUP BY album.album_id;

-- 4. Все исполнители, которые не выпустили альбомы в 2020 году (в 2011 году, у меня древние альбомы)
-- SELECT performer.name_performer, album.date_album FROM performer
-- INNER JOIN performeralbum ON performer.performer_id = performeralbum.performer_field 
-- INNER JOIN album ON performeralbum.album_field = album.album_id 
-- WHERE date_part('year', album.date_album) != 2011;

-- 4. ИСПРАВЛЕННЫЙ ВАРИАНТ. Все исполнители, которые не выпустили альбомы в 2020 году (в 2011 году, у меня древние альбомы)
SELECT performer.name_performer /* Получаем имена исполнителей */
FROM performer /* Из таблицы исполнителей */
WHERE performer.name_performer NOT IN ( /* Где имя исполнителя не входит в вложенную выборку */
    SELECT performer.name_performer /* Получаем имена исполнителей */
    FROM performer /* Из таблицы исполнителей */
    JOIN performeralbum ON performer.performer_id = performeralbum.performer_field /* Объединяем с промежуточной таблицей */
    JOIN album ON performeralbum.album_field = album.album_id /* Объединяем с таблицей альбомов */
    WHERE date_part('year', album.date_album) = 2011
); /* Где год альбома равен 2020 */

-- 5. Название сборников в которых присутствует исполнитель 'Разные артисты, A. Makarevich'
SELECT DISTINCT(collection.name_coll), performer.name_performer FROM collection
INNER JOIN trackcollection ON trackcollection.coll_field = collection.coll_id 
INNER JOIN track ON trackcollection.track_field = track.track_id 
INNER JOIN album ON track.album_field = album.album_id 
INNER JOIN performeralbum ON album.album_id = performeralbum.album_field 
INNER JOIN performer ON performeralbum.performer_field = performer.performer_id 
WHERE performer.name_performer = 'Разные артисты, A. Makarevich';

-- 6. Название альбомов, в которых присутствуют исполнители более одного жанра
-- SELECT album.name_album, COUNT(DISTINCT(genreperformer.genre_field)) AS Number_of_performers FROM album
-- INNER JOIN performeralbum ON album.album_id = performeralbum.album_field 
-- INNER JOIN performer ON performeralbum.performer_field = performer.performer_id
-- INNER JOIN genreperformer ON performer.performer_id = genreperformer.performer_field
-- GROUP BY album.name_album
-- HAVING COUNT(DISTINCT(genreperformer.genre_field)) > 1;

-- 6. ИСПРАВЛЕННЫЙ ВАРИАНТ. Название альбомов, в которых присутствуют исполнители более одного жанра
SELECT album.name_album, COUNT(DISTINCT(genreperformer.genre_field)) AS Number_of_performers FROM album
INNER JOIN performeralbum ON album.album_id = performeralbum.album_field 
INNER JOIN performer ON performeralbum.performer_field = performer.performer_id
INNER JOIN genreperformer ON performer.performer_id = genreperformer.performer_field
GROUP BY album.name_album, performer.performer_id
HAVING COUNT(DISTINCT(genreperformer.genre_field)) > 1;

-- 7. Наименование треков, которые не входят в сборники
SELECT track.name_track FROM track
LEFT JOIN trackcollection ON track.track_id = trackcollection.track_field
WHERE trackcollection.coll_field IS NULL;

-- 8. Исполнитель, написавший самый короткий трек (теоретически таких исполнителей может быт несколько)
SELECT performer.name_performer, t.name_track, t.duration_track AS duration_minimal FROM performer
INNER JOIN performeralbum pa ON performer.performer_id = pa.performer_field 
INNER JOIN album a ON pa.album_field = a.album_id 
INNER JOIN track t ON a.album_id = t.album_field
WHERE t.duration_track = (SELECT min(duration_track) FROM track);

-- 9. Название альбомов, с наименьшим количеством треков
-- Промежуточный запрос. Количество треков в альбомах
-- SELECT album.name_album, count(track.album_field) AS quantity_tracks_in_album FROM album
-- INNER JOIN track ON album.album_id = track.album_field
-- GROUP BY album.name_album;
-- Название альбомов, с наименьшим количеством треков
-- SELECT album.name_album, count(track.album_field) AS quantity_tracks_in_album FROM album 
-- INNER JOIN track ON album.album_id = track.album_field
-- GROUP BY album.name_album
-- HAVING count(track.album_field) = (
-- SELECT min(quantity_tracks_in_album) FROM (
--		SELECT count(track.album_field) AS quantity_tracks_in_album FROM album
--		INNER JOIN track ON album.album_id = track.album_field
--		GROUP BY album.name_album) AS foo
--	);
														 
-- 9. ИСПРАВЛЕННЫЙ ВАРИАНТ. Название альбомов, с наименьшим количеством треков
SELECT album.name_album /* Названия альбомов */
FROM album JOIN track ON album.album_id = track.album_field /* Объединяем альбомы и треки */
GROUP BY album.name_album /* Группируем по названиям альбомов */
HAVING COUNT(track.album_field) = ( /* Где количество треков равно вложенному запросу, в котором получаем наименьшее количество треков в одном альбоме */
    SELECT COUNT(track.album_field) /* Получаем поличество треков */
    FROM track JOIN album ON album.album_id = track.album_field /* Объединяем треки и альбомы */
    GROUP BY album.name_album /* Группируем по именам альбомов */
    ORDER BY COUNT(track.album_field) /* Сортируем по количеству треков */
    LIMIT 1 /* Получаем первую запись */
);