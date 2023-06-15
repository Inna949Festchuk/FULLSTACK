import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Cоздаем модель (абстракция ORM) - класс наследуемый от базового класса создаваемого 
# с помощью declarative_base()
Base = declarative_base()

class Course(Base):
    # Указываем название таблицы создаваемой в бд
    __tablename__ = "course"
    # Указываем поля(колонны)
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    # создаем связи relationship
    # вариант 1
    # homeworks = relationship("Homework", back_populates="course")

    def __str__(self):
        return f'Course {self.id}:{self.name}'

class Homework(Base):
    __tablename__ = "homework"

    id = sq.Column(sq.Integer, primary_key=True)
    number = sq.Column(sq.Integer, nullable=False)
    description = sq.Column(sq.Text, nullable=False)
    course_id = sq.Column(sq.Integer, sq.ForeignKey("course.id"), nullable=False) # sq.ForeignKey("course.id") ограничение внешнего ключа
    
    # создаем связи relationship
    #вариант 1# course = relationship(Course, back_populates="homeworks")
    # Вариант 2 (он лучше)
    course = relationship(Course, backref="homeworks")
    # Course - с какой таблицей мы хотим связаться
    # backref - обратное свойство в таблице Course 

    def __str__(self):
        return f'Homework {self.id}:({self.number}, {self.description}, {self.course_id})'
    
# Создаем функцию для создания таблиц в бд
def create_tables(engine):
    Base.metadata.drop_all(engine) # Удаление таблиц из бд
    Base.metadata.create_all(engine) # Если таблицы уже есть они создаваться не будут

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

    # Наполнение базы данных. Cоздание экземпляра класса Course
    course1 = Course(name='Python')

    # --------------
    # Здесь мы работаем с содержимым БД: 
    # - наполняем
    # - извлекаем
    # - объединяем таблицы и пр.
    # --------------

    # Закрытие сессии
    session.close()
