import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models_orm import create_tables, Course, Homework

if __name__ == '__main__':
    # Создаем строку подключения к бд (в данном случае к postgresql)
    login = 'postgres'
    password = 'postgres'
    db = 'Cities'

    DSN = f'postgresql://{login}:{password}@localhost:5432/{db}'

    # Создаем движок (абстракция ORM) для подключения к бд
    engine = sq.create_engine(DSN)

    ## Создаем таблицы
    create_tables(engine)

    # Создаем сессию как класс Session(поэтому с большой буквы)
    Session = sessionmaker(bind=engine)

    # Создаем экземпляр класса создателя сессии
    session = Session()

    # ----- Наполнение базы данных -----

    # Cоздание экземпляра класса Course
    course1 = Course(name='Python')

    # Добавляем запись в БД и фиксируем изменения в БД
    session.add(course1)
    session.commit()
    # print(course1)

    # Создаем несколько домашних заданий привязанных к курсу Пайтон
    hw1 = Homework(number = 1, description='простая домашка', course=course1)
    hw2 = Homework(number=2, description='сложная домашка', course=course1)

    # Добавляем СПИСОК add_all([]) в БД и фиксируем изменения в БД
    session.add_all([hw1, hw2])
    session.commit()

    # ----- Извлечение данных из БД -----

    # Извлекаем все курсы из БД с пом. all(), возвращающим итерируемый объект 
    for cours in session.query(Course).all():
        print(cours)
    # Извлекаем все домашки
    for hw in session.query(Homework).all():
        print(hw)

    # Фильтрация извлекаемых данных filter()
    for hw in session.query(Homework).filter(Homework.number > 1).all():
        print(hw)
    
    # Можно искать в строке с пом. like()
    for hw in session.query(Homework).filter(Homework.description.like('%сложн%')).all():
        print(hw)

    # ----- Объединение таблиц в БД ------

    # Объединим и отфильтруем
    for hw in session.query(Course).join(Homework.course).filter(Homework.number == 2).all():
        print(hw)
    # где course - связь relationship с помощью которой и связываются таблицы Course и Homework

    # ----- Создание вложенного подзапроса -----
    
    course2 = Course(name='Java')
    session.add(course2)
    session.commit()

    # Создание подзапроса subqury()
    subq = session.query(Homework).filter(Homework.description.like("%сложн%")).subquery()

    # Создание основного запроса который будет связан с результатами подзапроса subq
    # Связь необходимо задать явно Course.id == subq.c.course_id. 
    # Значения в поле id таблицы Course выбирутся те, что будут равны значениям в поле course_id результата подзапроса
    # Результаты подзапроса ВСЕГДА храняться в поле С
    for q in session.query(Course).join(subq, Course.id == subq.c.course_id).all():
        print(q)

    # Обновление и удаление данных
    # Сначала ищем что обновить, а потом указываем словарь с именем поля и новым значением в нем
    # обновление объектов
    session.query(Course).filter(Course.name == "Java").update({"name": "JavaScript"})
    session.commit()  # фиксируем изменения


    # # удаление объектов
    # session.query(Course).filter(Course.number > 1).delete()
    # session.commit()  # фиксируем изменения
    for cours in session.query(Course):
        print(cours)

    # Закрытие сессии
    session.close()