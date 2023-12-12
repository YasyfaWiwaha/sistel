from django.urls import path
from . import views
 
app_name = 'room'
urlpatterns = [
	path('', views.index, name='room_index'),
	path('add', views.add_room, name='add_room'),
	path('<room_number>/update', views.update_room, name='update_room'),
	path('<room_number>/delete', views.delete_room, name='delete_room')
]
