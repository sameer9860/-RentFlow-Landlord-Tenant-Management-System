from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from datetime import date
from core.mixins import LandlordRequiredMixin
from properties.models import Tenancy
from .models import RentInvoice, Payment, Expense
from .forms import PaymentForm, ExpenseForm
from django.db.models import Sum, Count
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
import io
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class ProfileRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and hasattr(self.request.user, 'profile')

class InvoiceListView(ProfileRequiredMixin, ListView):
    model = RentInvoice
    template_name = 'payments/invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        user = self.request.user
        qs = RentInvoice.objects.select_related('tenancy__room__property', 'tenancy__tenant')
        if user.profile.role == 'LANDLORD':
            return qs.filter(tenancy__room__property__landlord=user).order_by('-year', '-month')
        else:
            return qs.filter(tenancy__tenant=user).order_by('-year', '-month')

class GenerateInvoicesView(LandlordRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        today = timezone.now().date()
        month = today.month
        year = today.year
        
        # We only generate invoices for tenancies owned by this landlord
        active_tenancies = Tenancy.objects.filter(room__property__landlord=request.user, is_active=True)
        count = 0
        
        for tenancy in active_tenancies:
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
        
        if count > 0:
            messages.success(request, f"Successfully generated {count} new invoices for {month}/{year}.")
        else:
            messages.info(request, f"No new invoices to generate for {month}/{year}.")
            
        return redirect('payments:invoice_list')

class MarkInvoicePaidView(LandlordRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # Only allow confirming invoices that are awaiting confirmation
        invoice = RentInvoice.objects.filter(
            pk=pk,
            tenancy__room__property__landlord=request.user,
            status='AWAITING'
        ).first()
        if invoice:
            invoice.status = 'PAID'
            invoice.save()
            messages.success(request, f"Invoice #{invoice.id} payment confirmed.")
        else:
            messages.error(request, "Invoice not found, not awaiting confirmation, or access denied.")
        return redirect('payments:invoice_list')

class InvoiceDetailView(ProfileRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        if user.profile.role == 'LANDLORD':
            invoice = RentInvoice.objects.filter(
                pk=pk,
                tenancy__room__property__landlord=user
            ).select_related('tenancy__room__property', 'tenancy__tenant').first()
        else:
            invoice = RentInvoice.objects.filter(
                pk=pk,
                tenancy__tenant=user
            ).select_related('tenancy__room__property', 'tenancy__tenant').first()
        if not invoice:
            messages.error(request, "Invoice not found.")
            return redirect('payments:invoice_list')
        
        context = {'invoice': invoice}
        if user.profile.role == 'TENANT' and invoice.status == 'PENDING':
            context['payment_form'] = PaymentForm()
            
        return render(request, 'payments/invoice_detail.html', context)

class ProcessPaymentView(ProfileRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        invoice = RentInvoice.objects.filter(
            pk=pk,
            tenancy__tenant=request.user,
            status='PENDING'
        ).first()

        if not invoice:
            messages.error(request, "Invoice not found or already paid.")
            return redirect('payments:invoice_list')

        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.paid_amount = invoice.amount
            payment.save()

            # Instead of marking the invoice paid immediately we flag it as awaiting landlord confirmation
            invoice.status = 'AWAITING'
            invoice.save()

            messages.success(request, f"Payment for Invoice #{invoice.id} submitted and awaiting landlord confirmation.")
            return redirect('payments:invoice_detail', pk=pk)
        
        messages.error(request, "Invalid payment details.")
        return redirect('payments:invoice_detail', pk=pk)

class ExpenseListView(LandlordRequiredMixin, ListView):
    model = Expense
    template_name = 'payments/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        return Expense.objects.filter(landlord=self.request.user).order_by('-date')

class ExpenseCreateView(LandlordRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'payments/expense_form.html'
    success_url = reverse_lazy('payments:expense_list')

    def form_valid(self, form):
        form.instance.landlord = self.request.user
        messages.success(self.request, "Expense added successfully!")
        return super().form_valid(form)

class FinancialReportView(LandlordRequiredMixin, ListView):
    template_name = 'payments/financial_report.html'
    context_object_name = 'report_data'

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Filters
        month = int(self.request.GET.get('month', timezone.now().month))
        year = int(self.request.GET.get('year', timezone.now().year))
        
        invoices = RentInvoice.objects.filter(
            tenancy__room__property__landlord=user,
            month=month,
            year=year
        )
        
        payments = Payment.objects.filter(
            invoice__tenancy__room__property__landlord=user,
            payment_date__month=month,
            payment_date__year=year
        )
        
        expenses = Expense.objects.filter(
            landlord=user,
            date__month=month,
            date__year=year
        )
        
        revenue = payments.aggregate(total=Sum("paid_amount"))["total"] or 0
        total_expense = expenses.aggregate(total=Sum("amount"))["total"] or 0
        invoice_count = invoices.count()
        customer_count = Tenancy.objects.filter(room__property__landlord=user, is_active=True).values('tenant').distinct().count()
        
        due_summary = invoices.filter(status='PENDING').aggregate(total=Sum("amount"))["total"] or 0

        context.update({
            'month': month,
            'year': year,
            'revenue': revenue,
            'expenses': total_expense,
            'profit': revenue - total_expense,
            'invoice_count': invoice_count,
            'customer_count': customer_count,
            'due_summary': due_summary,
            'month_name': date(year, month, 1).strftime('%B'),
            'years': range(timezone.now().year - 2, timezone.now().year + 2),
            'months': [(i, date(2000, i, 1).strftime('%B')) for i in range(1, 13)],
        })
        
        return context

class ExportReportPDFView(LandlordRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        month = int(request.GET.get('month', timezone.now().month))
        year = int(request.GET.get('year', timezone.now().year))
        month_name = date(year, month, 1).strftime('%B')

        # Aggregation Logic (Similar to FinancialReportView)
        invoices = RentInvoice.objects.filter(tenancy__room__property__landlord=user, month=month, year=year)
        payments = Payment.objects.filter(invoice__tenancy__room__property__landlord=user, payment_date__month=month, payment_date__year=year)
        expenses = Expense.objects.filter(landlord=user, date__month=month, date__year=year)

        revenue = payments.aggregate(total=Sum("paid_amount"))["total"] or 0
        total_expense = expenses.aggregate(total=Sum("amount"))["total"] or 0
        profit = revenue - total_expense

        # PDF Generation
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Title
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, spaceAfter=20)
        elements.append(Paragraph(f"Monthly Financial Report - {month_name} {year}", title_style))
        elements.append(Spacer(1, 12))

        # Business Info
        elements.append(Paragraph(f"Landlord: {user.get_full_name() or user.username}", styles['Normal']))
        elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 24))

        # Summary Table
        data = [
            ["Metric", "Value"],
            ["Total Revenue", f"Rs. {revenue}"],
            ["Total Expenses", f"Rs. {total_expense}"],
            ["Net Profit", f"Rs. {profit}"],
            ["Total Invoices", str(invoices.count())],
        ]
        
        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 48))

        # Footer
        elements.append(Paragraph("Generated by RentFlow CRM", styles['Italic']))

        doc.build(elements)
        buffer.seek(0)
        
        filename = f"Financial_Report_{month_name}_{year}.pdf"
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

class ExportReportCSVView(LandlordRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        month = int(request.GET.get('month', timezone.now().month))
        year = int(request.GET.get('year', timezone.now().year))
        month_name = date(year, month, 1).strftime('%B')

        invoices = RentInvoice.objects.filter(tenancy__room__property__landlord=user, month=month, year=year)
        payments = Payment.objects.filter(invoice__tenancy__room__property__landlord=user, payment_date__month=month, payment_date__year=year)
        expenses = Expense.objects.filter(landlord=user, date__month=month, date__year=year)

        revenue = payments.aggregate(total=Sum("paid_amount"))["total"] or 0
        total_expense = expenses.aggregate(total=Sum("amount"))["total"] or 0

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Financial_Report_{month_name}_{year}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Financial Report', f"{month_name} {year}"])
        writer.writerow([])
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Revenue', revenue])
        writer.writerow(['Total Expenses', total_expense])
        writer.writerow(['Net Profit', revenue - total_expense])
        writer.writerow(['Total Invoices', invoices.count()])
        
        return response
