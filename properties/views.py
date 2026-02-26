from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import LandlordRequiredMixin
from .models import Property, Room
from .forms import PropertyForm, RoomForm

class PropertyListView(LandlordRequiredMixin, ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.filter(landlord=self.request.user)

class PropertyCreateView(LandlordRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('properties:property_list')

    def form_valid(self, form):
        form.instance.landlord = self.request.user
        messages.success(self.request, "Property created successfully!")
        return super().form_valid(form)

class RoomListView(LandlordRequiredMixin, ListView):
    model = Room
    template_name = 'properties/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return Room.objects.filter(property__landlord=self.request.user)

class RoomCreateView(LandlordRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'properties/room_form.html'
    success_url = reverse_lazy('properties:room_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['landlord'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Room created successfully!")
        return super().form_valid(form)
