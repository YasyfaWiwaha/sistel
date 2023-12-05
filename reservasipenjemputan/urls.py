from django.urls import path
from reservasipenjemputan.views import *

app_name = 'reservasipenjemputan'

urlpatterns = [
    path('reservasipenjemputan/', reservasipenjemputan, name='reservasipenjemputan'),
]