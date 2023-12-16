from django.urls import path
# from geoapp.views import show_point, create_point
from geoapp.views import PointAPIView

app_name = 'geoapp'

urlpatterns = [
    path('point/', PointAPIView.as_view()),
    path('point/<pk>/', PointAPIView.as_view()),
    # path('show_point/', show_point),
    # path('create_point/', create_point),
]