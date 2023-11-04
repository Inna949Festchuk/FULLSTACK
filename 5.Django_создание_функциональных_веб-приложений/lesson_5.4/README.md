## lesson 5.4 Работа с ORM (часть 2)

### Учебный материал:
- **Введение в занятие Работа с ORM (2 часть)**
- **Связи многие-ко-многим**
- **Many-to-many с помощью through**

Когда мы избавились от дублирования информации, удалив свойство products из модели Order, мы лишились возможности напрямую получать доступ к продуктам в заказе.

Косвенно можно получить продукты в заказе так:
```Python
- order_positions = some_order.positions.all()
- order_products = {pos.product for pos in order_positions}
```
Однако такой метод предполагает, что во всех местах, где нам потребуется получить продукты из заказа, придётся писать одинаковый код, что не всегда удобно. Также и в обратную сторону: чтобы найти все заказы, в которых участвует продукт, необходимо написать такой код:
```Python
- product_positions = some_product.positions.all()
- product_orders = {pos.order for pos in product_positions}
```
А ведь в первоначальном варианте, когда Django автоматически создавал связь m2m, было удобнее — было свойство products в классе Order и related_name orders.
На самом деле такую связь можно оставить, просто надо явно указать, что связь будет осуществляться через специальную модель. Тогда Django не будет создавать автоматическую связь m2m, но при этом останутся необходимые свойства:

```Python
class Order(models.Model):
    products = models.ManyToManyField(Product, related_name='orders', through='OrderPosition')
```
Теперь можно получать продукты из заказа простым способом:
```Python
order_products = some_order.products.all()
```
Аналогично с заказами, в которых участвует продукт:
```Python
product_orders = some_product.orders.all()
```
- **Django Debug Toolbar**
- **Презентация к видео "Работа с ORM"**

- **[Код к занятию (листинг)](../DJ_code/orm_advanced)**

### Дополнительные материалы:

- [Настройка конфигурации для дебаггера в VS Code](../lesson_5.1/debug_config)

### [Мой код по материалам занятий](../lesson_5.1/dj_proect/)

### [Домашняя работа](../dj-homeworks/2.2-databases-2/)
