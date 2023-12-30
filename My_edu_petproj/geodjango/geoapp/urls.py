from django.urls import path
from geoapp.views import (
    # show_point, 
    create_point,
    create_line,
    )
# from geoapp.views import (
#     PointAPIView,
#     LineAPIView
#     )

app_name = 'geoapp'

urlpatterns = [
    # path('point/', PointAPIView.as_view()),
    # path('point/<pk>/', PointAPIView.as_view()),
    # path('point/', show_point),
    path('create_point/', create_point),
    path('create_line/', create_line),
]