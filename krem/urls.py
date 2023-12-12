from django.urls import path
from . import views

app_name = 'krem'
urlpatterns = [
    path("reservation/new/<str:id>",views.reservation,name="reservation"),
    path("reservation/cancel/<str:id>",views.reservation_cancel,name="reservationcancel"),
    path("customer/daftar_reservasi/",views.daftar_reservasi_customer,name="daftar_reservasi_customer"),
    path("customer/daftar_reservasi/detail_reservasi/<str:pk>",views.detail_reservasi_customer,name="detail_reservasi_customer"),
]