from django.urls import path
from . import views

app_name = 'merah'

urlpatterns = [
    path("dashboard/",views.dashboard,name="dashboard"),
    path("complaint/<str:id>",views.complaint,name="complaint"),
]