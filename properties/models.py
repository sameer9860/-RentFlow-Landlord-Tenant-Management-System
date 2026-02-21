from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.name

class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.name} - Room {self.room_number}"

class Tenancy(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenancies')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='tenancies')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Tenancies"

    def __str__(self):
        return f"{self.tenant.username} at {self.room}"
