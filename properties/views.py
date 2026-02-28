from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import LandlordRequiredMixin
from .models import Property, Room, Tenancy
from .forms import PropertyForm, RoomForm, TenancyForm

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

class PropertyUpdateView(LandlordRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('properties:property_list')

    def get_queryset(self):
        return Property.objects.filter(landlord=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Property updated successfully!")
        return super().form_valid(form)

class PropertyDeleteView(LandlordRequiredMixin, DeleteView):
    model = Property
    template_name = 'properties/property_confirm_delete.html'
    success_url = reverse_lazy('properties:property_list')

    def get_queryset(self):
        return Property.objects.filter(landlord=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Property deleted successfully!")
        return super().form_valid(form)

class RoomListView(LandlordRequiredMixin, ListView):
    model = Room
    template_name = 'properties/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return Room.objects.filter(property__landlord=self.request.user).select_related('property')

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

class RoomUpdateView(LandlordRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'properties/room_form.html'
    success_url = reverse_lazy('properties:room_list')

    def get_queryset(self):
        return Room.objects.filter(property__landlord=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['landlord'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Room updated successfully!")
        return super().form_valid(form)

class RoomDeleteView(LandlordRequiredMixin, DeleteView):
    model = Room
    template_name = 'properties/room_confirm_delete.html'
    success_url = reverse_lazy('properties:room_list')

    def get_queryset(self):
        return Room.objects.filter(property__landlord=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Room deleted successfully!")
        return super().form_valid(form)

class TenancyListView(LandlordRequiredMixin, ListView):
    model = Tenancy
    template_name = 'properties/tenancy_list.html'
    context_object_name = 'tenancies'

    def get_queryset(self):
        return Tenancy.objects.filter(room__property__landlord=self.request.user).select_related('tenant', 'room__property')

class TenancyCreateView(LandlordRequiredMixin, CreateView):
    model = Tenancy
    form_class = TenancyForm
    template_name = 'properties/tenancy_form.html'
    success_url = reverse_lazy('properties:tenancy_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['landlord'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Tenancy created successfully!")
        return super().form_valid(form)

class TenancyUpdateView(LandlordRequiredMixin, UpdateView):
    model = Tenancy
    form_class = TenancyForm
    template_name = 'properties/tenancy_form.html'
    success_url = reverse_lazy('properties:tenancy_list')

    def get_queryset(self):
        return Tenancy.objects.filter(room__property__landlord=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['landlord'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Tenancy updated successfully!")
        return super().form_valid(form)

class TenancyDeleteView(LandlordRequiredMixin, DeleteView):
    model = Tenancy
    template_name = 'properties/tenancy_confirm_delete.html'
    success_url = reverse_lazy('properties:tenancy_list')

    def get_queryset(self):
        return Tenancy.objects.filter(room__property__landlord=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Tenancy deleted successfully!")
        return super().form_valid(form)
