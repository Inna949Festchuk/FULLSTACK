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
    
class Ball:
    # конструктор — он вызывается в момент создания нового объекта на основе этого класса
    def __init__(self, canvas, color, x, y, up, down, left, right):
        # задаём атрибуты (н-р: self.canvas, где .canvas - это свойство класса) нового объекта при создании
        # игровое поле
        self.canvas = canvas
        # координаты
        self.x = 0
        self.y = 0
        # цвет нужен был для того, чтобы мы им закрасили весь шарик
        # здесь появляется новое свойство id, в котором хранится внутреннее название шарика
        # а ещё командой create_oval мы создаём круг радиусом 15 пикселей и закрашиваем нужным цветом
        self.id = canvas.create_oval(10,10, 25, 25, fill=color)
        # помещаем шарик в точку с переданными координатами
        self.canvas.move(self.id, x, y)
        # если нажата стрелка вправо — двигаемся вправо
        self.canvas.bind_all(right, self.turn_right)
        # влево
        self.canvas.bind_all(left, self.turn_left)
        # наверх
        self.canvas.bind_all(up, self.turn_up)
        # вниз
        self.canvas.bind_all(down, self.turn_down)
        # шарик запоминает свою высоту и ширину
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    # движемся вправо
    # смещаемся на 2 пикселя в указанную сторону
    def turn_right(self, event):
        # получаем текущие координаты шарика
        pos = self.canvas.coords(self.id)
        # если не вышли за границы холста
        if not pos[2] >= self.canvas_width:
            # будем смещаться правее на 2 пикселя по оси х
            self.x = 2
            self.y = 0

    # влево
    def turn_left(self, event):
        pos = self.canvas.coords(self.id)
        if not pos[0] <= 0:
            self.x = -2
            self.y = 0
    # вверх
    def turn_up(self, event):
        pos = self.canvas.coords(self.id)
        if not pos[1] <= 0:
            self.x = 0
            self.y = -2

    # вниз
    def turn_down(self, event):
        pos = self.canvas.coords(self.id)
        if not pos[3] >= self.canvas_height:
            self.x = 0
            self.y = 2
                
    # метод, который отвечает за отрисовку шарика на новом месте
    def draw(self):
        # передвигаем шарик на заданный вектор x и y
        self.canvas.move(self.id, self.x, self.y)
        # запоминаем новые координаты шарика
        pos = self.canvas.coords(self.id)
        
        # если коснулись левой стенки
        if pos[0] <= 0:
            # останавливаемся
            self.x = 0
        # верхней
        if pos[1] <= 0:
            self.y = 0
        # правой
        if pos[2] >= self.canvas_width:
            self.x = 0
        # нижней
        if pos[3] >= self.canvas_height:
            self.y = 0

# НАСЛЕДОВАНИЕ
# новый класс на основе старого
class Jumper_ball(Ball):
    # ПОЛИМОРФИЗМ
    # этот метод называется так же, как и в старом классе, но мы его подменяем новыми действиями
    # метод, который отвечает за отрисовку шарика на новом месте
    def draw(self):
        # передвигаем шарик на заданный вектор x и y
        self.canvas.move(self.id, self.x, self.y)
        # запоминаем новые координаты шарика
        pos = self.canvas.coords(self.id)
        
        # если коснулись левой стенки
        if pos[0] <= 0:
            # отпрыгиваем в обратную сторону
            self.x = 2
        # верхней
        if pos[1] <= 0:
            self.y = 2
        # правой
        if pos[2] >= self.canvas_width:
            self.x = -2
        # нижней
        if pos[3] >= self.canvas_height:
            self.y = -2      
        
# создаём шарик — объект на основе класса
ball_one = Ball(canvas,'red', 100, 100,  '<KeyPress-Up>', '<KeyPress-Down>', '<KeyPress-Left>', '<KeyPress-Right>')
# создаём второй шарик — другой объект на основе этого же класса, но с другими параметрами
ball_two = Jumper_ball(canvas,'blue', 150, 150,  '<w>', '<s>', '<a>', '<d>')
ball_3 = Jumper_ball(canvas,'green', 200, 250,  '<w>', '<s>', '<a>', '<d>')
ball_4 = Jumper_ball(canvas,'orange', 300, 400,  '<w>', '<s>', '<a>', '<d>')
ball_5 = Jumper_ball(canvas,'yellow', 400, 400,  '<w>', '<s>', '<a>', '<d>')

ball_two.turn_down('<Motion>')
ball_3.turn_down('<Motion>')
ball_4.turn_down('<Motion>')
ball_5.turn_down('<Motion>')

# запускаем бесконечный цикл
while not False:

    # обновляем наше игровое поле, чтобы всё, что нужно, закончило рисоваться
    tk.update_idletasks()
    # обновляем игровое поле и смотрим за тем, чтобы всё, что должно было быть сделано — было сделано
    tk.update()
    # замираем на одну сотую секунды, чтобы движение элементов выглядело плавно
    time.sleep(0.01)
    # рисуем шарик 1
    ball_one.draw()
    # рисуем шарик 2
    ball_two.draw()
    # рисуем шарик 3
    ball_3.draw()
    # рисуем шарик 4
    ball_4.draw()
    # рисуем шарик 5
    ball_5.draw()
    if ball_one.canvas.coords(ball_one.id) == ball_two.canvas.coords(ball_two.id):
        print("GAME OVER!")
        break
    if ball_one.canvas.coords(ball_one.id) == ball_3.canvas.coords(ball_3.id):
        print("GAME OVER!")
        break
    if ball_one.canvas.coords(ball_one.id) == ball_4.canvas.coords(ball_4.id):
        print("GAME OVER!")
        break
    if ball_one.canvas.coords(ball_one.id) == ball_5.canvas.coords(ball_5.id):
        print("GAME OVER!")
        break
