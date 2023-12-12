from django.urls import path
from . import views

urlpatterns = [
    path("facility/",views.facility,name="facility"),
    path("facility/add",views.add_facility,name="addfacility"),
    path("facility/delete/<str:facility_name>",views.delete_facility,name="deletefacility"),
    path("facility/update/<str:facility_name>",views.update_facility,name="updatefacility"),
] 