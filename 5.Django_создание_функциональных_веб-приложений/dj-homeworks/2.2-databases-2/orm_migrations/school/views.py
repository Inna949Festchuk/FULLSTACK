from django.views.generic import ListView
from django.shortcuts import render

from .models import Student, Teacher


def students_list(request):
    object_students = Student.objects.all()
    object_teachers = Teacher.objects.all()
    students_count = [c.students.count() for c in object_teachers]
    template = 'school/students_list.html'
    context = {
        'object_students': object_students,
        'pairs': zip(object_teachers, students_count),
        }

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    # ordering = 'group' # упорядочивание  настроено в models.py в модели Meta

    return render(request, template, context)
