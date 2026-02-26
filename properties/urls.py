from django.urls import path
from .views import PropertyListView, RoomListView, PropertyCreateView, RoomCreateView

app_name = 'properties'

urlpatterns = [
    path('', PropertyListView.as_view(), name='property_list'),
    path('add/', PropertyCreateView.as_view(), name='property_add'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/add/', RoomCreateView.as_view(), name='room_add'),
]
