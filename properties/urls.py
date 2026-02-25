from django.urls import path
from .views import PropertyListView, RoomListView

app_name = 'properties'

urlpatterns = [
    path('', PropertyListView.as_view(), name='property_list'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
]
