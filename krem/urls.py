from django.urls import path
from . import views

urlpatterns = [
    path("reservation/",views.reservation_list,name="reservationlist"),
    path("reservation/new/<str:id>",views.reservation,name="reservation"),
    path("reservation/<str:id>",views.reservation_detail,name="reservationdetail"),
    path("reservation/cancel/<str:id>",views.reservation_cancel,name="reservationcancel"),
]