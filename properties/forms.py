from django import forms
from .models import Property, Room

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief Description (Optional)'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['property', 'room_number', 'monthly_rent', 'capacity', 'is_active']
        widgets = {
            'property': forms.Select(attrs={'class': 'form-select'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 101, A1'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, landlord, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter properties to only those owned by the logged-in landlord
        self.fields['property'].queryset = Property.objects.filter(landlord=landlord)
