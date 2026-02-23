from django.core.management.base import BaseCommand
from django.utils import timezone
from payments.models import RentInvoice

class Command(BaseCommand):
    help = 'Automatically updates the status of PENDING invoices to LATE if they are past their due date.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        overdue_invoices = RentInvoice.objects.filter(
            status='PENDING',
            due_date__lt=today
        )
        
        count = overdue_invoices.count()
        overdue_invoices.update(status='LATE')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} invoices to LATE status.'))
