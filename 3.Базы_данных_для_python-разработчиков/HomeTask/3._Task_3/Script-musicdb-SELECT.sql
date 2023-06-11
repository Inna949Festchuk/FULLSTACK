-- 1 название и год выхода альбомов, вышедших в 2018 году (в примере > 1998 заменить на = 2018)
SELECT name_album, date_album FROM album WHERE date_album > make_date(1998, 1, 1); -- У меня очень старые альбомы

-- 2 название и продолжительность самого длительного трека
SELECT name_track, duration_track FROM track ORDER BY duration_track DESC LIMIT 1; -- Сортируем по убыванию (DESC) и отображаем верхнюю запись
SELECT MAX(duration_track) AS max FROM track; -- или так

-- 3 название треков, продолжительность которых не менее 3,5 минуты
SELECT name_track, duration_track FROM track WHERE  duration_track > '00:03:30';

-- 4 названия сборников, вышедших в период с 2018 по 2020 год включительно (в примере с 1995-1-1 по 2011-9-19 включительно)
SELECT name_coll, date_coll FROM collection WHERE date_coll BETWEEN make_date(1995, 1, 1) AND make_date(2011, 9, 19);

-- 5 исполнители, чье имя состоит из 1 слова (в примере два слова, так как в БД нет исполнителя именуемого одним словом)
SELECT name_performer FROM performer WHERE name_performer NOT LIKE '% % %';

-- SELECT substring(name_performer, 0, 6) FROM performer; -- Если нужно выбрать определенное количество символов

-- 6 название треков, которые содержат слово "мой"/"my" (в примере "Звезда и Звезды"/"Me")
SELECT name_track FROM track WHERE name_track ILIKE '%зв_зд%' OR name_track LIKE '%Me%';


