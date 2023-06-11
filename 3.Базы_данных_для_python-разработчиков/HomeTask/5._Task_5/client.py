import psycopg2

def delete_table(conn, *args):
    '''Каскадное удаление таблиц в БД
    args - позиционный перечень удаляемых таблиц базы данных
    '''
    
    with conn.cursor() as cursor:
            
            try:
                
                for el_list in args:
                    cursor.execute(f"""
                    DROP TABLE {el_list} CASCADE;
                    """)
                    print(f'Удалена таблица: {el_list}')
                    conn.commit() # фиксируем в БД
                  
            except psycopg2.ProgrammingError:
                None
                print('Удалять нечего!')     

def  create_table(conn):
    '''Создание таблиц БД'''
    
    with conn.cursor() as cursor:
            
            try:
                
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS Clients(
                    id SERIAL PRIMARY KEY, 
                    first_name VARCHAR (40),
                    last_name VARCHAR (40),
                    email VARCHAR (40) UNIQUE
                    );
                """)
                conn.commit() # фиксируем в БД
                
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS Telephones(
                    id SERIAL PRIMARY KEY,
                    tel VARCHAR (40) UNIQUE,
                    id_client integer NOT NULL REFERENCES Clients(id) ON DELETE CASCADE 
                    );
                """)
                # ON DELETE CASCADE - Удаляя клиента, удаляются его номера телефонов
                conn.commit() # фиксируем в БД
                  
            except psycopg2.IntegrityError:
                None
                # print(f'Внимание! Найдено дублирующее значение.')

def add_client(conn, first_name, last_name, email, phones=None):
    '''Добавление нового клиента
    first_name - Имя клиента
    last_name - Фамилитя клиента
    email - Електронная почта клиента
    phones - Телефон клиента (не обязательный аргуменнт)
    ''' 
    
    with conn.cursor() as cursor:
            
            try:
                
                cursor.execute("""
                INSERT INTO Clients(
                    first_name, last_name, email) 
                    VALUES(%s, %s, %s);
                """, (first_name, last_name, email, ))
                conn.commit() # фиксируем в БД
                
                if phones == None: # Если телефон не задан
                    cursor.execute("""
                    INSERT INTO Telephones(
                        tel, id_client) 
                        VALUES(%s, (SELECT Clients.id FROM Clients WHERE Clients.first_name = %s AND 
                                                                                    Clients.last_name = %s));
                """, ('Телефон не задан', first_name, last_name,))  
                    conn.commit() # фиксируем в БД 
                else: # Если телефон задан фиксируем его в БД
                    cursor.execute("""
                    INSERT INTO Telephones(
                        tel, id_client) 
                        VALUES(%s, (SELECT Clients.id FROM Clients WHERE Clients.first_name = %s AND 
                                                                                Clients.last_name = %s));
                    """, (phones, first_name, last_name,))
                    conn.commit() # фиксируем в БД                                
                  
            except psycopg2.InternalError:
                None
                print(f'Внимание! Ошибка транзакции. Вводите значения по одному.')   
            
            except psycopg2.IntegrityError:
                None
                print(f'Внимание! Найдено дублирующее значение.')
            
            except psycopg2.ProgrammingError:
                None
                print(f'Внимание! Нарушение кардинальности. Полный тезка - это большая редкость.')                

def add_phone(conn, phone: str, client_id: int):
    '''Добавление телефона существующему клиенту
    phone - Добавочный телефон
    client_id - id клиента
    '''
    
    with conn.cursor() as cursor:
            
            try:
                
                cursor.execute("""
                INSERT INTO Telephones(
                    tel, id_client) 
                    VALUES(%s, %s
                );
                """, (phone, client_id, ))
                conn.commit() # фиксируем в БД
                  
            except psycopg2.InternalError:
                None
                print(f'Внимание! Ошибка транзакции. Вводите значения по одному.')   
            
            except psycopg2.IntegrityError:
                None
                print(f'Внимание! Найдено дублирующее значение или такой id отсутствует.')

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None, change=True):
    '''Изменение/удаление данных о клиенте (включая телефонный номер)
    change=True -  изменение номера
    change=False - удаление номера
    '''

    with conn.cursor() as cursor:
            
            try:
                
                if first_name == None: # Если не задано имя берем старое
                    cursor.execute("""
                    SELECT first_name FROM Clients WHERE id=%s;
                    """, (client_id, ))
                    first_name = cursor.fetchone()[0]
                    # print(first_name)
                
                if last_name == None: # Если не задана фамилия берем старую
                    cursor.execute("""
                    SELECT last_name FROM Clients WHERE id=%s;
                    """, (client_id, ))
                    last_name = cursor.fetchone()[0]
                    # print(last_name)

                if email == None: # Если не задан email берем старый
                    cursor.execute("""
                    SELECT email FROM Clients WHERE id=%s;
                    """, (client_id, ))
                    email = cursor.fetchone()[0]
                    # print(email)

                # Обновляем записи в БД
                cursor.execute("""
                UPDATE Clients SET first_name=%s, last_name=%s, email=%s WHERE id=%s;
                """, (first_name, last_name, email, client_id, ))
                conn.commit() # фиксируем в БД 

                # Если нужно выполнить изменение/удаление телефона
                cursor.execute("""
                SELECT tel FROM Telephones WHERE id_client=%s
                """, (client_id, ))
                print('У этого клиента найдены следующие телефонные номера:\n', *[el[0] for el in cursor.fetchall()], sep = '\n') # Извлекаем все строки

                variable_phone = input('\nПродублируйте телефон, который нужно изменить/удалить?')
                    
                if change == True:
                    cursor.execute("""
                    UPDATE Telephones SET tel=%s WHERE tel=%s;
                    """, (phone, variable_phone, ))
                    
                elif change == False:
                    cursor.execute("""
                    DELETE FROM Telephones WHERE tel=%s;
                    """, (variable_phone, ))                    
                    
                conn.commit() # фиксируем в БД 

            except psycopg2.IntegrityError:
                None
                print(f'Внимание! Найдено дублирующее значение.')
             

def delete_client(conn, client_id: int):
    '''Удаление клиента по id
    '''

    with conn.cursor() as cursor:
        
        try:     
            
            cursor.execute("""
            DELETE FROM Clients WHERE id=%s;
            """, (client_id,))
            
            conn.commit() 

        except psycopg2.IntegrityError:
            None
            print(f'Внимание! Такой id отсутствует.')

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    '''Поиск клиента
    '''

    with conn.cursor() as cursor:
        cursor.execute("""
        SELECT id, first_name, last_name, email FROM Clients WHERE 
            first_name=%s OR last_name=%s OR email=%s OR id=
            (SELECT Telephones.id_client FROM Telephones WHERE Telephones.tel=%s);
        """, (first_name, last_name, email, phone))
        for client in [el for el in cursor.fetchall()]:
            print(f'Найден клиент: {client}\n')

if __name__ == '__main__':

    with psycopg2.connect(database='client', user='postgres', password='Atoer949') as conn:

        create_table(conn)
        
        # delete_table(conn, 'Clients', 'Telephones')
        
        # add_client(conn, 'Степан', 'Степашкин', 'step@mail.ru', phones='8(111)122-77-54')
        # add_client(conn, 'Алексей', 'Сидоров', 'sidoroff@mail.ru', phones='8(906)021-85-88')
        # add_client(conn, 'Петр', 'Мельников', 'petroff@mail.ru')


        # add_phone(conn, '8(906)179-88-15', 1)

        # change_client(conn,  client_id=3, first_name='Bill', last_name='Geyts', email='microsoft@no.com', phone='8(657)09-90-909', change=True)
        # change_client(conn,  client_id=3, phone='8(657)09-90-909', change=True)
        # change_client(conn, client_id=3, change=False)

        # delete_client(conn, 1)

        # find_client(conn, first_name='Иван', last_name='Петров', email='petroff@mail.ru', phone='8(657)09-90-909')
        # find_client(conn, first_name='Иван', last_name='Иванов', email='petroff@mail.ru')
        # find_client(conn, phone='8(906)179-88-15')
        find_client(conn, first_name='Bill', email='petroff2@mail.ru')
    conn.close() # Нужно ли закрывать соединение при использовании контекстного менеджера?

