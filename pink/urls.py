from django.urls import path
from pink.views import *

app_name = "pink"
urlpatterns = [
    path("hotels/",hotel,name="hotel"),
    path("review/",review,name="review"),
]

