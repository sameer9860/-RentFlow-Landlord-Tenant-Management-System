from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Property, Room

class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.filter(landlord=self.request.user)

class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'properties/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return Room.objects.filter(property__landlord=self.request.user)
