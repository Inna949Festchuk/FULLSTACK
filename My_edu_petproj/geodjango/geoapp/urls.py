from django.urls import path
from geoapp.views import (
    show_point, 
    show_line,
    create_point,
    create_line,
    get_context_data,
    )
# from geoapp.views import (
#     PointAPIView,
#     LineAPIView
#     )


app_name = 'geoapp'

urlpatterns = [
    # path('point/', PointAPIView.as_view()),
    # path('point/<pk>/', PointAPIView.as_view()),
    
    path('show_point/', show_point),
    path('show_line/', show_line),
    path('create_point/', create_point),
    path('create_line/', create_line),
    # - - - - - - - - - - - - - - -
    # Создаем путь к шаблону карты (он будет использоваться для ее визуализации)
    path('map/', get_context_data),
    # - - - - - - - - - - - - - - -
]