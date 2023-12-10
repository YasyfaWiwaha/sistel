from django.urls import path
from ungu.views import *

app_name = 'ungu'

urlpatterns = [
    path('daftar_reservasi/', daftar_reservasi_hotel, name='daftar_reservasi_hotel'),
    path('daftar_reservasi/update_status/<str:pk>', update_reservasi_hotel, name='update_reservasi_hotel'),
]