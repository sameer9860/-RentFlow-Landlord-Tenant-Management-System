from django.db import models

class RentInvoice(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('LATE', 'Late'),
    )
    
    tenancy = models.ForeignKey('properties.Tenancy', on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['tenancy', 'month', 'year']

    def __str__(self):
        return f"Invoice #{self.id} for {self.tenancy} - {self.month}/{self.year}"

class Payment(models.Model):
    METHOD_CHOICES = (
        ('CASH', 'Cash'),
        ('ONLINE', 'Online'),
        ('BANK', 'Bank'),
        ('ESEWA', 'eSewa'),
    )
    
    invoice = models.ForeignKey(RentInvoice, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.paid_amount} for Invoice #{self.invoice.id}"
