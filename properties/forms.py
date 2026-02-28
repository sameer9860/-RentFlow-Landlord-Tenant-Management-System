from django import forms
from django.contrib.auth.models import User
from .models import Property, Room, Tenancy

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

class TenancyForm(forms.ModelForm):
    tenant_username = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    tenant_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    tenant_phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    tenant_address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 2}))
    tenant_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Initial Password'}))
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = Tenancy
        fields = ['room', 'start_date', 'end_date', 'is_active']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, landlord, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter rooms to only those owned by the logged-in landlord
        self.fields['room'].queryset = Room.objects.filter(property__landlord=landlord).select_related('property')
        
        # If editing an existing tenancy, hide user registration fields
        if self.instance.pk:
            del self.fields['tenant_username']
            del self.fields['tenant_email']
            del self.fields['tenant_phone']
            del self.fields['tenant_address']
            del self.fields['tenant_password']
            del self.fields['confirm_password']
        else:
            self.fields['tenant_username'].required = True
            self.fields['tenant_email'].required = True
            self.fields['tenant_phone'].required = True
            self.fields['tenant_address'].required = True
            self.fields['tenant_password'].required = True
            self.fields['confirm_password'].required = True

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.pk:
            password = cleaned_data.get('tenant_password')
            confirm_password = cleaned_data.get('confirm_password')

            if password and confirm_password and password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data
