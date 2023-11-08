from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    subject = models.CharField(max_length=10, verbose_name='Предмет')

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    teachers = models.ManyToManyField(Teacher, related_name='teachers', verbose_name = 'Учитель')
    group = models.CharField(max_length=10, verbose_name='Класс')

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

        ordering = ['group'] 
        #ordering, сообщает Django, что он должен сортировать результаты по полю group
        
        indexes = [models.Index(fields=['group']), ]
        # индекс базы данных по полю group повысит производительность запросов

    def __str__(self):
        return self.name
