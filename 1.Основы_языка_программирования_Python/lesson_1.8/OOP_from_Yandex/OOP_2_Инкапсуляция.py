# подключаем графическую библиотеку
from tkinter import *
# подключаем модули, которые отвечают за время и случайные числа
import time
# создаём новый объект — окно с игровым полем. В нашем случае переменная окна называется tk, и мы его сделали из класса Tk() — он есть в графической библиотеке 
tk = Tk()
# делаем заголовок окна — Games с помощью свойства объекта title
tk.title('Разбираем ООП')
# запрещаем менять размеры окна, для этого используем свойство resizable 
tk.resizable(0, 0)
# помещаем наше игровое окно выше остальных окон на компьютере, чтобы другие окна не могли его заслонить. Попробуйте 🙂
tk.wm_attributes('-topmost', 1)
# создаём новый холст — 400 на 500 пикселей, где и будем рисовать игру
canvas = Canvas(tk, width=500, height=400, highlightthickness=0)
# говорим холсту, что у каждого видимого элемента будут свои отдельные координаты 
canvas.pack()
# обновляем окно с холстом
tk.update()
# Описываем класс, который будет отвечать за шарики 
class Ball:
    # конструктор — он вызывается в момент создания нового объекта на основе этого класса
    def __init__(self, canvas, color, x, y, up, down, left, right):
        # задаём параметры нового объекта при создании
        # игровое поле
        self.__canvas = canvas
        # координаты
        self.__x = 0
        self.__y = 0
        # цвет нужен был для того, чтобы мы им закрасили весь шарик
        # здесь появляется новое свойство id, в котором хранится внутреннее название шарика
        # а ещё командой create_oval мы создаём круг радиусом 15 пикселей и закрашиваем нужным цветом
        self.__id = canvas.create_oval(10,10, 25, 25, fill=color)
        # помещаем шарик в точку с переданными координатами
        self.__canvas.move(self.__id, x, y)
        # если нажата стрелка вправо — двигаемся вправо
        self.__canvas.bind_all(right, self.__turn_right)
        # влево
        self.__canvas.bind_all(left, self.__turn_left)
        # наверх
        self.__canvas.bind_all(up, self.__turn_up)
        # вниз
        self.__canvas.bind_all(down, self.__turn_down)
        # шарик запоминает свою высоту и ширину
        self.__canvas_height = self.__canvas.winfo_height()
        self.__canvas_width = self.__canvas.winfo_width()
        
    # движемся вправо
    # смещаемся на 2 пикселя в указанную сторону
    def __turn_right(self, event):
        # получаем текущие координаты шарика
        pos = self.__canvas.coords(self.__id)
        # если не вышли за границы холста
        if not pos[2] >= self.__canvas_width:
            # будем смещаться правее на 2 пикселя по оси х
            self.__x = 2
            self.__y = 0
    # влево
    def __turn_left(self, event):
        pos = self.__canvas.coords(self.__id)
        if not pos[0] <= 0:
            self.__x = -2
            self.__y = 0
    # вверх
    def __turn_up(self, event):
        pos = self.__canvas.coords(self.__id)
        if not pos[1] <= 0:
            self.__x = 0
            self.__y = -2

    # вниз
    def __turn_down(self, event):
        pos = self.__canvas.coords(self.__id)
        if not pos[3] >= self.__canvas_height:
            self.__x = 0
            self.__y = 2
    
    # метод, который отвечает за отрисовку шарика на новом месте
    def draw(self):
        # передвигаем шарик на заданный вектор x и y
        self.__canvas.move(self.__id, self.__x, self.__y)
        # запоминаем новые координаты шарика
        pos = self.__canvas.coords(self.__id)
        
        # если коснулись левой стенки
        if pos[0] <= 0:
            # останавливаемся
            self.__x = 0
        # верхней
        if pos[1] <= 0:
            self.__y = 0
        # правой
        if pos[2] >= self.__canvas_width:
            self.__x = 0
        # нижней
        if pos[3] >= self.__canvas_height:
            self.__y = 0

# создаём шарик — объект на основе класса
ball_one = Ball(canvas,'red', 150, 150, '<KeyPress-Up>', '<KeyPress-Down>', '<KeyPress-Left>', '<KeyPress-Right>')
# создаём второй шарик — другой объект на основе этого же класса, но с другими параметрами
ball_two = Ball(canvas,'green', 100, 100, '<w>', '<s>', '<a>', '<d>')
# запускаем бесконечный цикл
while not False:
    # рисуем шарик
    ball_one.draw()
    ball_two.draw()
    # обновляем наше игровое поле, чтобы всё, что нужно, закончило рисоваться
    tk.update_idletasks()
    # обновляем игровое поле и смотрим за тем, чтобы всё, что должно было быть сделано — было сделано
    tk.update()
    # замираем на одну сотую секунды, чтобы движение элементов выглядело плавно
    time.sleep(0.01)