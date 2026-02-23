#Landlord–Tenant Management System Plan

# 🏗 Step 1: Project & App Setup

Create Django project:

bash
django-admin startproject config  
cd config
Create apps:

bash
python manage.py startapp accounts
python manage.py startapp properties
python manage.py startapp payments
python manage.py startapp dashboard
python manage.py startapp core
Add all apps to INSTALLED_APPS in config/settings.py.

# 🧑 Step 2: Accounts App

Goal: Extend Django’s User with a Profile model for roles.

accounts/models.py:

python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
ROLE_CHOICES = (
('LANDLORD', 'Landlord'),
('TENANT', 'Tenant'),
)
user = models.OneToOneField(User, on_delete=models.CASCADE)
role = models.CharField(max_length=10, choices=ROLE_CHOICES)
phone = models.CharField(max_length=15)
address = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.role}"

Signals: Auto-create profile when user is created.

Admin: Customize to show role, phone, address.

Means Accounts App (User & Roles)

We need role-based system.

Extend User with Profile

Create Profile model:

OneToOne to User

role (LANDLORD / TENANT)

phone

address

Why?

👉 Never modify Django’s User directly. Always extend.

Create Signal to Auto-Create Profile

Create signals.py inside accounts:

When user is created → automatically create profile.

Connect signals in apps.py.

Admin Customization

In admin.py:

Show role in list display

Add filters

Make it professional

# 🏢 Step 3: Properties App

Goal: Manage properties, rooms, and tenancies.

properties/models.py:

python
class Property(models.Model):
landlord = models.ForeignKey(User, on_delete=models.CASCADE)
name = models.CharField(max_length=100)
address = models.TextField()
description = models.TextField(blank=True)
created_at = models.DateTimeField(auto_now_add=True)

class Room(models.Model):
property = models.ForeignKey(Property, on_delete=models.CASCADE)
room_number = models.CharField(max_length=10)
monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
is_occupied = models.BooleanField(default=False)
capacity = models.IntegerField(default=1)
created_at = models.DateTimeField(auto_now_add=True)

class Tenancy(models.Model):
tenant = models.ForeignKey(User, on_delete=models.CASCADE)
room = models.ForeignKey(Room, on_delete=models.CASCADE)
start_date = models.DateField()
end_date = models.DateField(null=True, blank=True)
is_active = models.BooleanField(default=True)
Admin: Inline rooms under properties, inline tenancies under rooms.

Means— Property Management
✅ Create Property Model

Fields:

landlord (FK User)

name

address

description

created_at

Relationship:
One landlord → many properties

✅ Create Room Model

Fields:

property (FK)

room_number

monthly_rent

capacity

is_active

created_at

Do NOT store is_occupied here directly.

Why?

Because occupancy should depend on active tenancy.

Better design.

✅ Create Tenancy Model (Very Important)

This is the professional way.

Fields:

tenant (FK User)

room (FK)

start_date

end_date

is_active

Why this model?

✅ Track history
✅ Change tenants
✅ Keep records
✅ No data loss

Without Tenancy model → your system becomes weak.

# 💰 Step 4: Payments App

Goal: Track invoices and payments.

payments/models.py:

python
class RentInvoice(models.Model):
tenancy = models.ForeignKey('properties.Tenancy', on_delete=models.CASCADE)
month = models.IntegerField()
year = models.IntegerField()
amount = models.DecimalField(max_digits=10, decimal_places=2)
due_date = models.DateField()
status = models.CharField(max_length=10, choices=[('PENDING','Pending'),('PAID','Paid'),('LATE','Late')])
generated_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
invoice = models.ForeignKey(RentInvoice, on_delete=models.CASCADE)
paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
payment_date = models.DateTimeField(auto_now_add=True)
method = models.CharField(max_length=20, choices=[('CASH','Cash'),('ONLINE','Online'),('BANK','Bank'),('ESEWA','eSewa')])
transaction_id = models.CharField(max_length=50, blank=True, null=True)
Means Payment System
Create RentInvoice Model

Fields:

tenancy (FK)

month

year

amount

due_date

status (Pending / Paid / Late)

generated_at

Add unique constraint:
One invoice per tenancy per month/year.

Create Payment Model

Fields:

invoice (FK)

paid_amount

payment_date

method

transaction_id

Allow multiple payments per invoice.

# step 5-Business Logic

Now we add intelligence.

✅ Auto Generate Monthly Invoices

Create:

payments/management/commands/generate_invoices.py

Logic:

Find all active tenancies

Create invoice if not exists for current month

Run monthly using:

cron job (Linux)

Windows Task Scheduler

Celery (production way)

✅ Auto Update Status

Add model method:

If today > due_date AND status != Paid → mark as Late.

You can override save() or create a utility function.

# step 6-Dashboard

✅ Landlord Dashboard Stats

Use Django ORM:

Total Properties

Total Rooms

Active Tenancies

Vacant Rooms

Expected Monthly Income

Collected Income

Pending Income

Occupancy Rate

Use:

annotate()
aggregate()
Count()
Sum()

This makes it professional.

✅ Tenant Dashboard

Show:

Current room

Monthly rent

Next due date

Payment history

Outstanding balance

Filter by logged-in user.

# step 7-Frontend

✅ Use Django Templates + Bootstrap

Create:

base.html

landlord_dashboard.html

tenant_dashboard.html

property_list.html

room_list.html

invoice_list.html

Keep UI simple but clean.

# step 8-Permissions

✅ Restrict Access by Role

Create decorator or mixin:

Only landlord → property management

Only tenant → payment view

Use:

UserPassesTestMixin
LoginRequiredMixin

# step 9-Optimization

✅ Add Indexes

Add database indexes to:

month

year

status

landlord

tenancy

This improves performance.

✅ Add select_related & prefetch_related

Example:

Tenancy.objects.select_related('tenant', 'room')

Avoid N+1 queries.

# step 10-Advanced Features

After MVP works:

🔹 Add Email Reminder

Send reminder 3 days before due date.

🔹 Add eSewa Integration

Since you're in Nepal, integrate sandbox payment.

🔹 Add Reports Export (CSV/Excel)
🔹 Add REST API using Django REST Framework

🏁 Final Development Order (Correct Order)

Setup project

Create accounts app

Create properties app

Create tenancy system

Create payment system

Add business logic

Build dashboards

Add permissions

Optimize queries

Add automation
