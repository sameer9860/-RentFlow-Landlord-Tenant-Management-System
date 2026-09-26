from django.urls import path
from .views import (
    PropertyListView, PropertyCreateView, PropertyUpdateView, PropertyDeleteView,
    RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView,
    TenancyListView, TenancyCreateView, TenancyUpdateView, TenancyDeleteView,
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
    path('tenancies/', TenancyListView.as_view(), name='tenancy_list'),
    path('tenancies/add/', TenancyCreateView.as_view(), name='tenancy_add'),
    path('tenancies/<int:pk>/edit/', TenancyUpdateView.as_view(), name='tenancy_edit'),
    path('tenancies/<int:pk>/delete/', TenancyDeleteView.as_view(), name='tenancy_delete'),
]
