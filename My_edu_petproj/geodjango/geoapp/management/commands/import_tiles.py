# Это скрипт загрузки файла формата osm.pbf в базу данных postgresql
# Он использует векторный драйвер OSM — OpenStreetMap XML и PBF 
# и утилиту GDAL - ogr2ogr (GDAL нужно установить)
# 
# Драйвер OSM — OpenStreetMap XML и PBF читает файлы OpenStreetMap 
# в форматах .osm (на основе XML) и .pbf (оптимизированный двоичный файл) в БД Postgresql и SqlLite
# Описание драйвера: https://gdal.org/drivers/vector/osm.html
# 
# Файл OSM  получен с ресурса в формате .pbf: 
# 
# Формат PBF ("Protocolbuffer Binary Format") предназначен для замены Формата XML. 
# Файл OSM в формате .pbf примерно в два раза меньше по размеру чем OSM XML. 
# Он поддерживает примерно в 5 раз большую скорость чтения/записи. 
# Формат PBF был разработан для поддержки лучшей расширяемости и гибкости в будущем.
# Описание формата: https://wiki.openstreetmap.org/wiki/RU:PBF_Format

from django.core.management.base import BaseCommand
from geoapp.models import (
    # WorldBorder, 
    # Tile,
    WorldPoint,
    WorldLine,
    # PointInLine,
)
# from geoapp.models import Tile
# from django.contrib.gis.gdal import DataSource
# from mbutil import mbtiles_connect
# import osgeo.ogr 

# class Command(BaseCommand):
#     '''
#     Класс дает возможность создания собственной терминальной команды
#     cоздания БД и импорта в нее OSM данных в формате .pbf
#     '''
#     def add_arguments(self, parser):
#         parser.add_argument(
#             '-c',
#             '--create',
#             action='store_true',
#             default=False,
#             help='Создание БД и импорт в нее OSM данных  в формате .pbf'
#         )

#     def handle(self, *args, **options):

#         if options['create'] or options['c']:
#             import subprocess
#             # ИСТОЧНИКИ:
#             # https://habr.com/ru/articles/467043/
#             # https://habr.com/ru/articles/511144/
#             # https://www.youtube.com/watch?v=87liLpASYPI
#             # https://habr.com/ru/articles/265329/

#             # Вначале создаем БД в Postgresql, название особого значения не имеет.
#             # PATH=$PATH:/Applications/Postgres.app/Contents/Versions/12/bin/
#             # psql -c "CREATE DATABASE test;"

#             # Далее добавим необходимые для дальнейшей работы расширения.

#             # psql -d test -c "CREATE EXTENSION postgis; CREATE EXTENSION hstore; "
#             # Расширение hstore предназначено для работы с наборами ключ/значение, т.к. много информации будет содержаться в OSM-тегах.

#             # ogr2ogr -f PostgreSQL "PG:dbname=test" test.pbf -lco COLUMN_TYPES=other_tags=hstore

#             # Путь к файлу osm.pbf
#             osm_pbf_file = 'geoapp/data/planet_20.6047,54.6752_20.6541,54.6975.osm.pbf'
#             # Имя целевой таблицы
#             target_table = 'planet_osm_node'

#             # Параметры соединения с базой данных PostgreSQL (замените на ваши реальные данные подключения)
#             db_name = 'test'
#             db_user = 'postgres'
#             db_password = 'admin'
#             db_host = 'localhost'
#             # db_port = '5432'

#             # Команда ogr2ogr для загрузки данных OSM в базу данных PostgreSQL с использованием модели GeoDjango
#             ogr2ogr_cmd = [
#                 'ogr2ogr', # Путь к библиотеке GDAL ogr2ogr
#                 '-f', 'PostgreSQL', 
#                 f'PG:dbname={db_name} user={db_user} password={db_password} host={db_host}', 
#                 osm_pbf_file, # Путь к источнику данных .pbf
#                 '-lco', 
#                 'COLUMN_TYPES=other_tags=hstore'
#             ]
            
#             # Выполнение команды ogr2ogr
#             subprocess.run(ogr2ogr_cmd)
#         else:
#             print('Для наполнения базы данных введите python manage.py import_tiles -c')

class Command(BaseCommand):
    '''
    Класс дает возможность создания собственной терминальной команды
    cоздания БД и импорта в нее OSM данных в формате .pbf
    '''
    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            action='store_true',
            default=False,
            help=''
        )

    def handle(self, *args, **options):

        if options['c']:     

            from osgeo import gdal, ogr, osr
            from PIL import Image
            import os
            import math

            import os
            import PIL

            # def generate_tiles(input_file, tile_size, zoom_level):
            #     """
            #     Генерирует набор плиток для данного растрового файла и уровня масштабирования.

            #     : param input_file: Путь к растровому файлу.
            #     : param tile_size: размер каждой плитки в пикселях.
            #     : param Zoom_level: Уровень масштабирования для плиток.
            #     : return: список кортежей, каждый из которых содержит путь к плитости и ее уровню масштабирования.
            #     """
            #     # Open the raster file and extract its spatial reference
            #     raster = gdal.Open(input_file)
            #     srs = osr.SpatialReference(raster.GetProjection())

            #     # Calculate the tile width and height based on the raster resolution and zoom level
            #     width = tile_size // 2
            #     height = tile_size // 2
            #     tile_count = math.ceil(raster.RasterYSize / height)
            #     zoom_level = zoom_level - 0  # Ignore zero zoom levels

            #     # Create a list to store the tile paths and zoom levels
            #     tile_paths = []

            #     # Loop through the tiles, starting from the top-left corner
            #     for y in range(tile_count):
            #         # Calculate the top-left corner of the current tile
            #         x = width // 2
            #         y = height // 2

            #         # Walk through the rows of the raster, generating tiles for each one
            #         for x_off in range(-width // 2, width // 2):
            #             # Calculate the tile path based on the raster file and zoom level
            #             tile_path = os.path.join(input_file.split('/')[:-1], f'{zoom_level}_{x}_{y}.tif')

            #             # Write the tile to disk
            #             with PIL.Image.open(tile_path, 'wb') as tile:
            #                 # Draw the raster data on the tile
            #                 raster.ReadAsArray(x, y, width, height, tile)

            #             # Add the tile path to the list
            #             tile_paths.append((tile_path, zoom_level))

            #     # Return the list of tile paths and zoom levels
            #     return tile_paths
            
            # generate_tiles(input_file, tile_size, zoom_level)




            # Функция генерации растрового изображения из запроса к базе данных
            # def query_to_raster(sql_query):

                # # Подключение к базе данных (замените на свои параметры подключения)
                # connection_string = "PG:host='localhost' dbname='test' user='postgres' password='admin'"
                
                # # Выполнение SQL запроса и экспорт результата во временный GeoTIFF
                # output_raster = 'geoapp/data/temp.tif'
                # # gdal.SetConfigOption('GDAL_PAM_ENABLED', 'NO')

                # # Create the RasterizeOptions object
                # rasterize_options = gdal.RasterizeOptions()
                #     # output_raster,
                #     # connection_string,
                #     # outputSRS = ['-a_srs EPSG:4326']
                # # )

                # # Rasterize the geometry layer
                # oga_layer = ogr.Layer(sql_query)
                # gdal.Rasterize(oga_layer, rasterize_options)

                # from osgeo import gdal, ogr

                # # Establish connection string for PostgreSQL database
                # conn_str = "PG:host=localhost dbname=test user=postgres password=admin"

                # # Open the database
                # pg_ds = gdal.OpenEx(conn_str, gdal.OF_VECTOR)

                # if pg_ds is None:
                #     raise Exception("Could not open the database")

                # # Access the table or SQL query
                # ogr_layer = pg_ds.ExecuteSQL(sql_query)

                # # Set up the rasterization options with appropriate parameters for your case
                # rasterize_options = gdal.RasterizeOptions(
                #     format='GTiff',
                #     outputType=gdal.GDT_Byte,  # Choose type according to your needs
                #     xRes=10,  # Horizontal resolution (pixel size)
                #     yRes=10,  # Vertical resolution (pixel size)
                #     allTouched=True,
                #     # Additional options can go here
                # )

                # # Output raster file name
                # output_raster = "geoapp/data/temp.tif"

                # # Rasterize the layer
                # gdal.Rasterize(output_raster, ogr_layer, options=rasterize_options)

                # # Release the results and close the dataset
                # pg_ds.ReleaseResultSet(ogr_layer)
                # pg_ds = None
            



            # - - - - - -
            from osgeo import gdal, ogr
            # Define connection string for the PostgreSQL database
            conn_string = "PG:host=localhost user=postgres dbname=test password=admin"

            # Open the PostgreSQL database as an OGR data source
            pg_data_source = ogr.Open(conn_string, 0)  # 0 means read-only

            if pg_data_source is None:
                raise Exception("Could not open the OGR data source")

            # Assume 'geom_field' is the geometry field and 'my_table' is the table or view you wish to rasterize
            sql_command = "SELECT location FROM lines_model"
            layer = pg_data_source.ExecuteSQL(sql_command, dialect='PostgreSQL')

            if layer is None:
                raise Exception("Could not execute SQL command or access the layer")

            # Define rasterization options
            xRes, yRes = 10, 10  # Replace with the resolution you want
            output_raster_path = "geoapp/data/temp.tiff"  # Replace with the desired output TIFF path

            # Create a new raster in memory to hold the rasterized data with the right dimensions
            dst_ds = gdal.GetDriverByName('GTiff').Create(output_raster_path, int(layer.GetExtent()[1] - layer.GetExtent()[0]) // xRes, int(layer.GetExtent()[3] - layer.GetExtent()[2]) // yRes, 1, gdal.GDT_Byte)
            dst_ds.SetGeoTransform((layer.GetExtent()[0], xRes, 0, layer.GetExtent()[3], 0, -yRes))
            
            # Rasterize the layer
            gdal.RasterizeLayer(dst_ds, [1], layer)

            # Once rasterization is done, clean up
            dst_ds = None
            layer = None
            pg_data_source.ReleaseResultSet(layer)
            pg_data_source = None
            # - - - - -





                # gdal.VectorTranslate(
                #     output_raster,
                #     connection_string,
                #     format=f"{gdal.GetDriverByName('GTiff')}",
                #     # sql=sql_query,
                #     dstSRS=['-a_srs EPSG:4326'],  # Укажите нужную проекцию
                #     SQLStatement=['-sql', str(sql_query)]
                # )
            #     return output_raster
            # query_to_raster("SELECT location FROM lines_model")
            
            # import psycopg2
            # from osgeo import gdal, osr
            # from PIL import Image

            # # Подключение к базе данных PostgreSQL
            # conn = psycopg2.connect(database="test", user="postgres", password="admin", host="localhost", port="5432")

            # # Создание объекта курсора
            # cur = conn.cursor()

            # # Выполнение SQL-запроса для извлечения данных из таблицы
            # cur.execute("SELECT location FROM lines_model")

            # # Получение данных из курсора в виде списка
            # rows = cur.fetchall()
            # print(rows)

            # # Закрытие курсора и соединения
            # cur.close()
            # conn.close()

            # # Создание пустого растра с нужными размерами и разрешением
            # driver = "GTIFF"
            # out_raster = "geoapp/data/raster.tiff"
            # width = 256
            # height = 256
            # srid = 4326  # Для преобразования в EPSG:28404
    
            # # Создание пустого растра с помощью GDAL
            # dst_ds = gdal.GetDriverByName(driver).Create(out_raster, int(width), int(height), gdal.GDT_Float32)
            # dst_ds.SetProjection(osr.SpatialReference(srid=srid).ExportToWkt())
            

            # # Цикл по каждой строке в таблице
            # for row in rows:
            #     # Получение данных из строки
            #     geom = row[0]  # Геометрия для каждой строки

            #     # Преобразование геометрии в растровый формат с помощью GDAL
            #     src_ds = gdal.OpenEx(geom, gdal.OF_INTERLEAVED | gdal.GA_ReadOnly)
            #     band = src_ds.GetRasterBand(1)
            #     data = band.ReadAsArray()

            #     # Преобразование данных в формат растра с помощью GDAL
            #     dst_band = dst_ds.GetRasterBand(1)
            #     dst_band.WriteArray(data)

            #     # Добавление метаданных к растру с помощью Pillow
            #     img = Image.fromarray(data)
            #     img.save("geoapp/data/tiles/thumbnail.jpg")

            #     # Закрытие исходного и целевого наборов данных
            #     src_ds = None
            #     dst_ds = None

            # # Закрытие целевого набора данных
            # dst_ds = None




            # # Функция преобразования GeoTIFF в тайлы
            # def generate_tiles(input_raster, tiles_folder, zoom_level):
            #     tile_size = 256

            #     # Открытие исходного растра
            #     ds = gdal.Open(input_raster)
            #     width = ds.RasterXSize
            #     height = ds.RasterYSize

            #     # Количество тайлов с учетом уровня зума
            #     n_tiles_x = math.ceil(width / tile_size)
            #     n_tiles_y = math.ceil(height / tile_size)

            #     for x in range(n_tiles_x):
            #         for y in range(n_tiles_y):
            #             # Координаты тайла
            #             x_off = x * tile_size
            #             y_off = y * tile_size

            #             # Создание подизображения (тайла)
            #             tile = ds.ReadAsArray(x_off, y_off, tile_size, tile_size)

            #             # Сохранение тайла в PNG
            #             tile_filename = os.path.join(tiles_folder, f'{zoom_level}_{x}_{y}.png')
            #             Image.fromarray(tile).save(tile_filename)
            #             print(f'Generated tile {tile_filename}')

            # # Пример использования
            # sql_query = "SELECT * FROM lines_model"  # Измените на ваш SQL запрос lines_model-название модели в БД
            # input_raster = query_to_raster(sql_query)
            # tiles_folder = 'geoapp/data/tiles'
            # zoom_level = 12  # Пример уровня зума

            # generate_tiles(input_raster, tiles_folder, zoom_level)

            # # Удаление временного файла
            # os.remove('geoapp/data/temp.tif')
        
        else:
            print('Для генерации тайлов из базы данных введите manage.py import_tiles -c')







        #     # Установите соединение с базой данных
        #     conn = psycopg2.connect(database=database_name, user=user, password=password, host=host, port=port)

        #     # Создайте курсор для выполнения SQL-запросов
        #     cur = conn.cursor()

        #     # Загрузите данные OSM в базу данных
        #     # with open(osm_file, 'r') as file:
        #     #     cur.copy_expert(
        #     #         file=file,
        #     #         table='planet_osm_node',
        #     #         sep='\t'
        #     #         # columns=['way_id', 'osm_id', 'node_id', 'way_tag', 'node_tag', 'the_geom']
        #     #     )
        #     # with conn.cursor() as cur: 
        #     #     cur.copy_from(osm_file, "planet_osm_node", sep=",")

        #    # Загрузите данные OSM в базу данных
        #     with open(osm_file, 'r', encoding='utf-8') as file:  # Use 'rb' instead of 'r' for opening binary files
        #         cur.copy_expert(
        #             sql=sql.SQL("COPY planet_osm_node FROM STDIN WITH (FORMAT binary)"),
        #             file=file
        #         )

        #     # Закройте соединение с базой данных
        #     cur.close()
        #     conn.close()










            # # Получите данные OSM из API OSM
            # url = f'http://api06.dev.openstreetmap.org/api/v4/map.json?key={api_key}'
            # response = get(url)
            # osm_data = response.json()

            # # Преобразуйте данные OSM в формат, который может быть использован osm2pgsql
            # osm_data_converted = osmium.osm_to_postgis(osm_data)

            # # Загрузите данные в базу данных PostgreSQL
            # osm2pgsql.main(["-d", "-c", osm_data_converted, "public.planet_osm_point"])

            # # Установите соединение с базой данных
            # conn = psycopg2.connect(database=database_name, user=user, password=password, host=host, port=port)

            # # Создайте курсор для выполнения SQL-запросов
            # cur = conn.cursor()

            # # Закройте соединение с базой данных
            # cur.close()
            # conn.close()

        # else:
        #     print('Для наполнения базы данных введите python manage.py import_tiles -c')
            










            # tileset = mbtiles_connect(mbtiles_file='geoapp/data/planet_19.63,54_22.8,55.43-mbtiles-openmaptiles/planet_19.63,54_22.8,55.43.mbtiles', silent=None)
            # # zoom, col, row = 8, 9, 40
            # # tile = tileset.get_tile(zoom, col, row)
            # # binary_png = tile.get_png()
            # cursor_sqlite = tileset.cursor()
            # # text_json = tileset.json()
            # # print(text_json)
            # # Получение списка таблиц из MBTiles
            # cursor_sqlite.execute("SELECT name FROM sqlite_master WHERE type='table';")
            # tables = cursor_sqlite.fetchall()

            # for table in tables:
            #     # Извлечение данных из таблицы MBTiles
            #     cursor_sqlite.execute(f"SELECT * FROM {table[0]} WHERE ID=1;")
            #     rows = cursor_sqlite.fetchall()
            #     print(rows)
            
            # tileset.close()

            # # открываем тайл
            # ds = DataSource('geoapp/data/planet_19.63,54_22.8,55.43-mbtiles-openmaptiles/planet_19.63,54_22.8,55.43.mbtiles')

            # for layer in ds:
            #     # print(layer.zoom)
            #     for feature in layer:
            #         # создаем экземпляр модели и сохраняем данные
            #         tile = Tile(zoom_level=layer.zoom, tile_column=feature.x, tile_row=feature.y, tile_data=feature.data)
            #         tile.save() 
            
            
            
            # from osgeo import ogr

            # # Открываем MBTiles файл
            # ds = ogr.Open('geoapp/data/planet_19.63,54_22.8,55.43-mbtiles-openmaptiles/planet_19.63,54_22.8,55.43.mbtiles')

            # # Получаем количество слоев (тайлсетов) в MBTiles
            # num_layers = ds.GetLayerCount()

            # # Перебираем все слои и объекты, сохраняя данные в базу данных
            # for i in range(num_layers):
            #     layer = ds.GetLayerByIndex(i)
            #     for feature in layer:
            #         zoom_level = feature.GetField('zoom_level')
            #         tile_column = feature.GetField('tile_column')
            #         tile_row = feature.GetField('tile_row')
            #         tile_data = feature.GetField('tile_data')

            #         # Создаем экземпляр модели и сохраняем данные (пример для использования Django ORM)
            #         tile = Tile(zoom_level=zoom_level, tile_column=tile_column, tile_row=tile_row, tile_data=tile_data)
            #         tile.save()


       
            # from osgeo import ogr

            # # Открываем MBTiles файл
            # ds = ogr.Open('geoapp/data/planet_19.63,54_22.8,55.43-mbtiles-openmaptiles/planet_19.63,54_22.8,55.43.mbtiles')

            # # Получаем количество слоев (тайлсетов) в MBTiles
            # num_layers = ds.GetLayerCount()

            # # Перебираем все слои и объекты, сохраняя данные в базу данных
            # for i in range(num_layers):
            #     layer = ds.GetLayerByIndex(i)
            #     # Проверяем наличие необходимых полей
            #     layer_defn = layer.GetLayerDefn()
            #     field_names = [layer_defn.GetFieldDefn(j).GetName() for j in range(layer_defn.GetFieldCount())]
            #     print(field_names)

                # for feature in layer:
                #     if 'zoom_level' in field_names:
                #         zoom_level = feature.GetField('zoom_level')
                #     else:
                #         zoom_level = None  # или умолчание, если требуется
                    
                #     if 'tile_column' in field_names:
                #         tile_column = feature.GetField('tile_column')
                #     else:
                #         tile_column = None
                    
                #     if 'tile_row' in field_names:
                #         tile_row = feature.GetField('tile_row')
                #     else:
                #         tile_row = None

                #     if 'tile_data' in field_names:
                #         tile_data = feature.GetField('tile_data')
                #     else:
                #         tile_data = None

                #     # Проверяем, получены ли все необходимые данные перед их сохранением
                #     if zoom_level is not None and tile_column is not None and tile_row is not None and tile_data is not None:
                #         # Создаем экземпляр модели и сохраняем данные (пример для использования Django ORM)
                #         tile = Tile(zoom_level=zoom_level, tile_column=tile_column, tile_row=tile_row, tile_data=tile_data)
                #         tile.save()
                #     else:
                #         # Обрабатываем отсутствующие данные
                #         # Например, пропустить запись, логировать ошибку или задать альтернативные значения
                #         pass









            # import sqlite3
            # import psycopg2

            # # Соединение с базой данных SQLite (MBTiles)
            # mypath = 'geoapp/data/planet_19.63,54_22.8,55.43-mbtiles-openmaptiles/planet_19.63,54_22.8,55.43.mbtiles'
            # conn_sqlite = sqlite3.connect(mypath)
            # cursor_sqlite = conn_sqlite.cursor()

            # # Соединение с базой данных PostgreSQL
            # conn_postgres = psycopg2.connect(database="test", user="postgres", password="admin", host="localhost", port="5432")
            # cursor_postgres = conn_postgres.cursor()

            # # # Получение списка таблиц из MBTiles
            # # cursor_sqlite.execute("SELECT name FROM sqlite_master WHERE type='table';")
            # # tables = cursor_sqlite.fetchall()

            # # for table in tables:
            # # Извлечение данных из таблицы MBTiles tiles
            # cursor_sqlite.execute(f"SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles;")
            # rows = cursor_sqlite.fetchall()

            # for row in rows:
            #     zoom_level, tile_column, tile_row, tile_data = row

            #     # Вставка данных в базу данных PostgreSQL
            #     cursor_postgres.execute("INSERT INTO Tile (zoom_level, tile_column, tile_row, tile_data) VALUES (%s, %s, %s, %s);", (zoom_level, tile_column, tile_row, psycopg2.Binary(tile_data)))

            # # Фиксация изменений и закрытие соединений
            # conn_postgres.commit()
            # cursor_postgres.close()
            # conn_postgres.close()

            # conn_sqlite.close()








        # else:
        #     print('Для наполнения базы данных введите python manage.py import_tiles -c')

# {'id': '1', 
#  'name': 'Samsung Galaxy Edge 2', 
#  'image': 'https://avatars.mds.yandex.net/get-mpic/364668/img_id5636027222104023144.jpeg/orig', 
#  'price': '73000', 
#  'release_date': '2016-12-12', 
#  'lte_exists': 'True'}

# Можно еще одним вариантом сделать, это метод .save() просто 
# переопределить в моделе, чтобы слаг заполнялся автоматически
#     def save(self, *args, **kwargs):  # new
#         if not self.slug:
#             self.slug = slugify(self.name)
#         return super().save(*args, **kwargs)

# super позволяет изменить дополнить метод save, 
# не ковыряя его под копотом

# А далее
# Phone(name=phone['name'],
# price=phone['price'], 
# image=phone['image'], 
# release_date=phone['release_date'], 
# lte_exists=phone['lte_exists']).save()

# Можно посмотреть здесь 
# https://qna.habr.com/q/307406
# https://proghunter.ru/articles/django-base-2023-automatic-slug-generation-cyrillic-handling-in-django-9