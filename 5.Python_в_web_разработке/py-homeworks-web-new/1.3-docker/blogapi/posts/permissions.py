from rest_framework import permissions
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # - БЕЗОПАСНЫЕ МЕТОДЫ (GET, OPTIONS и HEAD)
            return True
        return obj.author == request.user

# Мы импортируем разрешения сверху, а затем создаем пользовательский
# класс IsAuthorOrReadOnly, который расширяет BasePermission . Затем мы
# переопределяем has_object_permission . Если запрос содержит HTTP-методы,
# включенные в SAFE_METHODS - кортеж, содержащий GET, OPTIONS и
# HEAD - то это запрос только для чтения, и разрешение предоставляется.
# В противном случае запрос предназначен для какой-то записи, что
# означает обновление ресурса API с функциями создания, удаления или
# редактирования. В этом случае мы проверяем, совпадает ли автор
# рассматриваемого объекта, которым является наша запись в блоге
# obj.author, с пользователем, делающим запрос request.user .
# Вернувшись в файл views.py, мы должны импортировать IsAuthorOrReadOnly
# и затем мы можем добавить permission_classes для PostDetail.