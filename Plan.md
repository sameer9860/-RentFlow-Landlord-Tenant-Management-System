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

Means  Accounts App (User & Roles)

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
✅  Create Property Model

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

    
📊 Step 5: Dashboard App
Goal: Landlord & Tenant dashboards with stats.

Landlord Dashboard:

Total properties, rooms, occupancy rate.

Expected rent vs collected vs pending.

Tenant Dashboard:

Current rent, next due date, outstanding balance.

Payment history.

Use QuerySet annotations for calculations:

python
from django.db.models import Sum, Count

occupied = Room.objects.filter(is_occupied=True).count()
vacant = Room.objects.filter(is_occupied=False).count()
expected_rent = Room.objects.aggregate(Sum('monthly_rent'))
⚙️ Step 6: Automatic Invoice Generation
Option 1: Django management command (run via cron).

Option 2: Celery + Redis (production-ready).

Logic:

On 1st of each month, loop through active tenancies.

Generate RentInvoice with due date = 7th of month.

🛡 Step 7: Admin Customization
Show inline relationships (rooms under property, payments under invoice).

Add filters for landlord, tenant, status.

Use list_display for quick stats.

📈 Step 8: Scalability & SaaS Features
Add subscription plans for landlords.

Integrate Stripe/eSewa for online payments.

Add email/SMS reminders.

Generate PDF invoices with reportlab or xhtml2pdf.

Export reports in CSV/Excel.

✅ Step-by-Step Execution Plan
Setup project & apps → accounts, properties, payments, dashboard, core.

Build models → Start with accounts.Profile, then Property, Room, Tenancy, then RentInvoice & Payment.

Migrate & test in Admin → Ensure CRUD works.

Add dashboards → Landlord stats, tenant views.

Implement invoice generation → Management command first, Celery later.

Enhance admin → Filters, inlines, stats.

Add payment integration → Start with manual entry, later integrate APIs.

Deploy & scale → PostgreSQL, SaaS features.