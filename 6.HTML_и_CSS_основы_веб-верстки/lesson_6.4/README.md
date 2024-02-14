## Lesson 6.4 Позиционирование блочных элементов

### Учебный материал:

### [По материалам: Гайд по flexbox](https://doka.guide/css/flexbox-guide/)

Идея *флексбоксов* появилась ещё в 2009 году, и этот стандарт до сих пор развивается и прорабатывается. Основная идея флексов — гибкое распределение места между элементами, гибкая расстановка, выравнивание, гибкое управление. Ключевое слово — гибкое, что и отражено в названии (flex — англ. гибко).

### Основные термины
- **Флекс-контейнер:** элемент, к которому применяется свойство `display: flex`. Вложенные в него элементы подчиняются правилам раскладки флексов.
- **Флекс-элемент:** элемент, вложенный во флекс-контейнер.
![](https://doka.guide/css/flexbox-guide/images/1-2200w.webp)
- **Основная ось:** основная направляющая флекс-контейнера, вдоль которой располагаются флекс-элементы.
- **Поперечная (побочная, перпендикулярная) ось:** ось, идущая перпендикулярно основной. Позже вы поймёте, для чего она нужна.
- **Начало / конец основной оси:** точки в начале и в конце основной оси соответственно. Это пригодится нам для выравнивания флекс-элементов.
- **Начало / конец поперечной оси:** точки в начале и в конце поперечной оси соответственно.
![](https://doka.guide/css/flexbox-guide/images/3-2200w.webp)
- **Размер по основной оси (основной размер):** размер флекс-элемента вдоль основной оси. Это может быть ширина или высота в зависимости от направления основной оси.
- **Размер по поперечной оси (поперечный размер):** размер флекс-элемента вдоль поперечной оси. Это может быть ширина или высота в зависимости от направления поперечной оси. Этот размер всегда перпендикулярен основному размеру. Если основной размер — это ширина, то поперечный размер — это высота, и наоборот.
![](https://doka.guide/css/flexbox-guide/images/4-2200w.webp)

### Свойства флекс-контейнера
####  `display`

```css
.container {
  display: flex;
}
```
Когда мы задаём какому-то элементу значение `flex` для свойства `display`, мы превращаем этот элемент в **флекс-контейнер**. Внутри него начинает действовать **флекс-контекст**, его дочерние элементы начинают подчиняться свойствам *флексбокса*.

Снаружи флекс-контейнер выглядит как **блочный элемент** — занимает всю ширину родителя, **следующие за ним элементы в разметке переносятся на новую строку**.

```css
.container {
  display: inline-flex;
}
```
Если контейнеру задано значение `inline-flex`, то снаружи он начинает вести себя как строчный (инлайн) элемент — размеры зависят только от внутреннего контента, встаёт в строку с другими элементами. Внутри это ровно такой же флекс-контейнер, как и при предыдущем значении.

#### `flex-direction`
Свойство управления направлением основной и поперечной осей.

```css
.container {
  display: flex;
  flex-direction: row;
}
```
**Возможные значения:**

- `row` (значение по умолчанию) — основная ось идёт горизонтально слева направо, поперечная ось идёт вертикально сверху вниз.
- `row-reverse` — основная ось идёт горизонтально справа налево, поперечная ось идёт вертикально сверху вниз.
- `column` — основная ось идёт вертикально сверху вниз, поперечная ось идёт горизонтально слева направо.
- `column-reverse` — основная ось идёт вертикально снизу вверх, поперечная ось идёт горизонтально слева направо.

![](https://doka.guide/css/flexbox-guide/images/5-2200w.webp)




<!DOCTYPE html>
<html lang="ru">

<head>
  <title>Пример свойства flex-direction — Гайд по flexbox — Дока</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto&family=Roboto+Mono&display=swap" rel="stylesheet">

  <script type="module" crossorigin src="./flex_direction.js"></script>
  <link rel="stylesheet" href="../main.css">


<script>
  (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
  m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
  (window, document, "script", "https://cdn.jsdelivr.net/npm/yandex-metrica-watch/tag.js", "ym")

  ym(83244811, "init", {
    clickmap:true,
    trackLinks:true,
    accurateTrackBounce:true
  })
</script>
<noscript><img src="https://mc.yandex.ru/watch/83244811" style="position:absolute;left:-9999px" alt=""></noscript>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GH8FX28ET0"></script>
<script>
  window.dataLayer = window.dataLayer || []
  function gtag(){dataLayer.push(arguments)}
  gtag("js", new Date())
  gtag("config", "G-GH8FX28ET0")
</script>
</head>

<body class="_dark">
  <main class="main-wrap">
    <code class="code">
        <pre><span class="code__selector">.container</span> {</pre>
        <pre>	<span class="code__properties">width</span>: <span class="code__value">100%</span>;</pre>
        <pre>	<span class="code__properties">height</span>: <span class="code__value">320px</span>;</pre>
        <pre>	<span class="code__properties">display</span>: <span class="code__value">flex</span>;</pre>
        <pre class="_active">	<span class="code__properties">flex-direction</span>: <select data-select="flex-direction" class="code__select" name="flex-direction" >
          <option selected value="row">row</option>
          <option value="row-reverse">row-reverse</option>
          <option value="column">column</option>
          <option value="column-reverse">column-reverse</option>
        </select>;</pre>
        <pre>}</pre>
      </code>

    <div data-demo-wrap class="demo">
      <div class="item item_start">
        <span class="item__name">Start</span>
      </div>
      <div data-demo-item class="item">
        <span data-demo-item-name class="item__name">Item</span>
        <div class="item__controls">
          <button data-demo-item-btn="remove" class="item__btn item__btn_remove" aria-label="Удалить элемент"></button>
          <button data-demo-item-btn="size" class="item__btn item__btn_size"
            aria-label="Увеличить/уменьшить элемент"></button>
          <button data-demo-item-btn="add" class="item__btn item__btn_add" aria-label="Добавить элемент"></button>
        </div>
      </div>
      <div data-demo-end class="item item_end">
        <span class="item__name">End</span>
      </div>
    </div>
  </main>
</body>

</html>








- [Правила оформления HTML-кода](https://github.com/netology-code/codestyle/tree/master/html)
- [Правила оформления CSS-кода](https://github.com/netology-code/codestyle/tree/master/css)

### Код из лекции: 

- [Мой код](../My_code/)

### Дополнительные материалы:

- [Основы HTML & CSS](https://html5book.ru/osnovy-css/)
- [ОЧЕНЬ КРУТОЙ РЕСУРС!!! >>> Веб-технологии для разработчиков HTML & CSS & JS](https://developer.mozilla.org/ru/docs/Learn/HTML)
- [Валидатор кода](https://validator.w3.org/nu/)
 
- [Свойство display](https://doka.guide/css/display/)
- [Гайд по flexbox](https://doka.guide/css/flexbox-guide/)

### [Домашняя работа](../fpy-homeworks/block-elements-positioning/README.md)
