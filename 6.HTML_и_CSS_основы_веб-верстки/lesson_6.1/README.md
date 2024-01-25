## Lesson 6.1 Введение в вёрстку

### Учебный материал:

**Структура HTML-документа**

```html
<!DOCTYPE html> <!-- Объявление формата документа -->
<html>
<head> <!-- Техническая информация о документе -->
<meta charset="UTF-8"> <!-- Определяем кодировку символов документа -->
<title>...</title> <!-- Задаем заголовок документа -->
<link rel="stylesheet" type="text/css" href="style.css"> <!-- Подключаем внешнюю таблицу стилей -->
<script src="script.js"></script> <!-- Подключаем сценарии -->
</head>
<body> <!-- Основная часть документа -->
</body>
</html>
```
**Объектная модель документа, DOM (document object model)**

![ПРОСТЕЙШАЯ СТРУКТУРА ВЕБ-СТРАНИЦЫ](https://html5book.ru/wp-content/uploads/2014/10/DOM.png)

*[далее здесь ...](https://html5book.ru/osnovy-html/)*

**Основы CSS**

![Структура объявления](https://html5book.ru/wp-content/uploads/2014/12/css_osnovy.png)

**Пример селектора тега body:**

```css
body {
    /* цвет шрифта */
    color: red;
    /* подложка */
    background: wheat;
    /* название шрифта */
    font-family: Arial, sans-serif;
    /* жирность */
    font-weight: 700;
    /* размер шрифта в пикселях px */
    font-size: 25px;
    /* начертание */
    font-style: italic;
    /* убрать подчеркивание */
    text-decoration: none;
}
```

**Пример селекторов для разных тегов:**

```html
<body>
    <div class="content">
        <h1>
            Погружение в JavaScript: подборка книг для начинающих изучать язык
        </h1>
        <p>
            Эта статья для тех, кто решил «приручить» программирование. После изучения HTML и CSS я долго выбирала, с чего начать, какой язык программирования освоить. В итоге остановилась на JavaScript (JS) — он показался мне наиболее перспективным и востребованным на данный момент.
        </p>
        <p>
            В блоге уже была подборка <a href="https://netology.ru/blog/learn-javascript-basics?utm_source=blog&utm_medium=747&utm_campaign=blog&stop=1" >сервисов</a>, помогающих в освоении JS, я же решила поделиться полезной литературой — книгами, которые помогли мне стартовать в программировании.	
        </p>
    </div>
</body>
```

```css
body {
  /* название шрифта */
  font-family: Arial, sans-serif;
  /* размер шрифта в пикселях px */
  font-size: 16px;
}

h1 {
  /* размер шрифта в пикселях px */
  font-size: 28px;
}

a {
  /* цвет шрифта */
  color: #349bdf;
  /* убрать подчеркивание */
  text-decoration: none;
}
```

**Пример селекторов для разных классов:**

```html
<body>
    <div class="card">
        <img class="card-img" src="https://netology-code.github.io/html-2-homeworks/introduction-html-css/widget/img/Секреты-JavaScript-ниндзя.jpg" alt="Обложка книги Cекреты JavaScript">
            <div class="card-content">
                <h1 class="card-name">
                Секреты JavaScript ниндзя. Джон Резиг, Беэр Бибо, Иосип Марас
                </h1>
                <p>
                    Первое издание книги вышло в 2012 году, второе — в 2017. Я читала второе издание. В нём на подробных примерах авторы рассматривают методики и понятия языка JS. Обучение происходит от азов к мастерству. По задумке авторов читатели после прочтения должны стать хорошими специалистами.
                </p>
            </div>
    </div>
</body>
```

```css
.card-content {
  margin-left: 30px;
}

.card-name {
  margin-top: 0;
  font-size: 24px;
}
```

*[далее здесь ...](https://html5book.ru/osnovy-css/)*

- [Правила оформления HTML-кода](https://github.com/netology-code/codestyle/tree/master/html)
- [Правила оформления CSS-кода](https://github.com/netology-code/codestyle/tree/master/css)

### Код из лекции: 

- [Мой код](../My_code)

### Дополнительные материалы:

- [Основы HTML & CSS](https://html5book.ru/osnovy-css/)
- [ОЧЕНЬ КРУТОЙ РЕСУРС!!! >>> Веб-технологии для разработчиков HTML & CSS & JS](https://developer.mozilla.org/ru/docs/Learn/HTML)
- [Валидатор кода](https://validator.w3.org/nu/)
- [Как писать более чистый CSS: дюжина советов от банальных до неочевидных](https://habr.com/p/788508/)
### [Домашняя работа](../fpy-homeworks/introduction-html-css/)
