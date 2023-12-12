from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', show_login, name='show_login'),
    path('logout/', show_login, name='logout'),
    path('register/', show_register, name='show_register'),
    path('register/hotel/', show_register_hotel, name='show_register_hotel'),
    path('register/customer/', show_register_customer, name='show_register_customer'),
]