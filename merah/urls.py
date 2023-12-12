from django.urls import path
from . import views
<<<<<<< HEAD
app_name='merah'
=======

app_name = 'merah'

>>>>>>> e727fe4cedfd469db614a2e44f5efae9634026f7
urlpatterns = [
    path("dashboard/",views.dashboard,name="dashboard"),
    path("complaint/<str:id>",views.complaint,name="complaint"),
]