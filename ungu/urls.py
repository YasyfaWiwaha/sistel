from django.urls import path
from ungu.views import *

app_name = 'ungu'

urlpatterns = [
    path('hotel/daftar_reservasi/', daftar_reservasi_hotel, name='daftar_reservasi_hotel'),
    path('customer/daftar_reservasi/', daftar_reservasi_customer, name='daftar_reservasi_customer'),
    path('hotel/daftar_reservasi/update_status/<str:pk>', update_reservasi_hotel, name='update_reservasi_hotel'),
    path('customer/daftar_reservasi/update_status/<str:pk>', update_reservasi_customer, name='update_reservasi_customer'),
    path('hotel/daftar_reservasi/detail_reservasi/<str:pk>', detail_reservasi_hotel, name='detail_reservasi_hotel'),
    path('customer/daftar_reservasi/detail_reservasi/<str:pk>', detail_reservasi_customer, name='detail_reservasi_customer'),
    path('customer/daftar_reservasi/detail_reservasi/buat_reservasi_shuttle/<str:pk>', form_buat_reservasi_shuttle, name='form_buat_reservasi_shuttle'),
]