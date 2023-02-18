import psycopg2

# dbname = 'musicdb'
# user = 'postgres'
# dbpass = 'Atoer949'
# host='localhost'
# port = '5432'
# db = f'postgresql://{user}:{dbpass}@{host}:{port}/{dbname}'
# engine = sqlalchemy.create_engine(db)

conn = psycopg2.connect(database='musicdb', user='postgres', password='Atoer949')

ts = ['FF', 'PP']
for t in ts:
	with conn.cursor() as cur:
		cur.execute(f"INSERT INTO blog(post_title) VALUES('{t}');")
		conn.commit()
