from django.urls import path
from .views import (
    PropertyListView, PropertyCreateView, PropertyUpdateView, PropertyDeleteView,
    RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView,
)

app_name = 'properties'

urlpatterns = [
    path('', PropertyListView.as_view(), name='property_list'),
    path('add/', PropertyCreateView.as_view(), name='property_add'),
    path('<int:pk>/edit/', PropertyUpdateView.as_view(), name='property_edit'),
    path('<int:pk>/delete/', PropertyDeleteView.as_view(), name='property_delete'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/add/', RoomCreateView.as_view(), name='room_add'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_edit'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),
]
