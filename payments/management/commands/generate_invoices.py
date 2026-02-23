from django.core.management.base import BaseCommand
from django.utils import timezone
from properties.models import Tenancy
from payments.models import RentInvoice
from datetime import date

class Command(BaseCommand):
    help = 'Automatically generates rent invoices for all active tenancies for the current month.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        month = today.month
        year = today.year
        
        active_tenancies = Tenancy.objects.filter(is_active=True)
        count = 0
        
        for tenancy in active_tenancies:
            # Check if invoice already exists for this tenancy, month, and year
            invoice, created = RentInvoice.objects.get_or_create(
                tenancy=tenancy,
                month=month,
                year=year,
                defaults={
                    'amount': tenancy.room.monthly_rent,
                    'due_date': date(year, month, 7),
                    'status': 'PENDING'
                }
            )
            
            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Created invoice for {tenancy}'))
            else:
                self.stdout.write(self.style.WARNING(f'Invoice already exists for {tenancy} for {month}/{year}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} invoices.'))
