from django.db import models
from django.shortcuts import get_object_or_404

# date and time
from datetime import datetime
from decimal import *

from .helpers.util import *

PDFS_PATH = "./app_cashtracker/static/app_cashtracker/reports/"
 
# Create your models here.
# USER
class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    salary = models.DecimalField(default=0.000, max_digits=19, decimal_places=3)
    currency = models.CharField(max_length=255, default="BGN")
    created = models.DateTimeField('date created')
    is_active = models.BooleanField(default=True)

    def register(self, params):
        self.email = params['email']
        self.password = hash_password(params['password_1'])
        self.created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save()

    def __str__(self):
        return self.user_name


# PAYMENT
class Payment(models.Model):
    value = models.DecimalField(default=0.000, max_digits=19, decimal_places=3)
    currency = models.CharField(max_length=3, default="BGN")
    category = models.ForeignKey('Category')
    subcategory = models.ForeignKey('Subcategory')
    date_time = models.DateTimeField('date and time created')
    name = models.CharField(max_length=255, default="")
    comment = models.CharField(max_length=1000, default="")
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)

    def parse_date(self, payments_for):
        if payments_for == 'today':
            self.date_time = self.date_time.strftime('%H:%M:%S')
        else:
            self.date_time = self.date_time.strftime('%d/%m/%Y')
        return self

    def convert_currency(self, to_currency):
        self.value = currency_converter(self.currency, to_currency, self.value)
        self.currency = to_currency
        return self

    def fetch_payments(payments_for, payments_cat, payments_curr, logged_user):
        payments_from = take_date(payments_for)

        if payments_cat and payments_cat is not '0':

            payments = Payment.objects.filter(
                user_id=logged_user.id, 
                is_active=1,
                date_time__gt=payments_from.strftime('%Y-%m-%d %H:%M:%S'),
                category=get_object_or_404(Category, id=payments_cat)
            )

        else:

            payments = Payment.objects.filter(
                user_id=logged_user.id, 
                is_active=1,
                date_time__gt=payments_from.strftime('%Y-%m-%d %H:%M:%S')
            )

        return payments


    def __str__(self):
        return self.name


# CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)

    def get_category_name(category_id=0):
        if not int(category_id):
            return 'All'
        else:
            return get_object_or_404(Category, id=category_id)

    def __str__(self):
        return self.name


# SUBCATEGORY
class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# REPORT
class Report(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField('date created')
    report_type = models.CharField(max_length=255)
    report_date = models.DateTimeField('report date used for report_type')
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    currency = models.CharField(max_length=3, default="BGN")
    is_active = models.BooleanField(default=True)


    def generate_report_pdf(self):
    
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']
        styleH.alignment = 1;

        # container for the 'Flowable' objects
        elements = []

        elements.append(
            Paragraph(
                "<u>BILLING REPORT</u><br/><br/>",
                styleH)
            )

        elements.append(
            Paragraph(
                "Payments from: <b>{}</b>".format(self.report_type.title()),
                styleN)
            )

        elements.append(
            Paragraph(
                "Currency: <b>{}</b>".format(self.currency),
                styleN)
            )

        elements.append(
            Paragraph(
                "Categories: <b>{}</b>".format(self.category_names()),
                styleN)
            )

        doc = SimpleDocTemplate(
            "{}{}.pdf".format(PDFS_PATH, self),
            pagesize=letter
        )

        payments = self.fetch_payments()

        payments_table = [[
         'Date',
         'Name', 
         'Category', 
         'Subcategory', 
         'Comment', 
         'Value'
         ]]

        payments_data = {}
        payments_data['all_total'] = Decimal('0')
        for payment in payments:

            payment_data = []
            # update payments objects
            payment.parse_date(self.report_type)
            payment.convert_currency(self.currency)

            # add data for all payments
            payment_data.append(payment.date_time)
            payment_data.append(payment.name)
            payment_data.append(payment.category)
            payment_data.append(payment.subcategory)
            payment_data.append(payment.comment)
            payment_data.append(payment.value)

            payments_data['all_total'] += Decimal(payment.value)

            payments_table.append(payment_data)
        
        elements.append(
            Paragraph(
                "Total: <b>{}{}</b><br/><br/>".format(
                    payments_data['all_total'],
                    self.currency
                ),
                styleN)
            )

        t=Table(payments_table, colWidths=(None, 80, 80, None, 120, 50))
        t.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.25, colors.black),
            ('ALIGN', (5,1), (-1,-1), 'RIGHT')]))
        elements.append(t)
        # write the document to disk
        doc.build(elements)
        return self


    def category_names(self):
        rhc = ReportHasCategories.objects.filter(report=self)
        names = ', '.join(list(map(lambda r: r.category.name, rhc)))
        if names is '':
            return 'All'
        else:
            return names


    def add_category(self, category):
        report_category = ReportHasCategories()
        report_category.report = self
        report_category.category = category
        report_category.save()


    def add_payment(self, payment):
        report_payment = ReportHasPayments()
        report_payment.report = self
        report_payment.payment = payment
        report_payment.save()


    def fetch_payments(self):
        rhp = ReportHasPayments.objects.filter(report=self)
        return list(map(lambda r: r.payment, rhp))


    def __str__(self):
        return 'Report_from_{}_in_{}'.format(self.report_type, self.currency)


# REPORT HAS PAYMENTS
class ReportHasPayments(models.Model):
    report = models.ForeignKey('Report')
    payment = models.ForeignKey('Payment')

    def __str__(self):
        return 'ReportHasPayments with id - {}'.format(self.id)


# REPORT HAS CATEGORIES
class ReportHasCategories(models.Model):
    report = models.ForeignKey('Report')
    category = models.ForeignKey('Category')

    def __str__(self):
        return 'ReportHasCategories with id - {}'.format(self.id)


# REPORT HAS SUBCATEGORIES
class ReportHasSubcategories(models.Model):
    report = models.ForeignKey('Report')
    subcategory = models.ForeignKey('Subcategory')

    def __str__(self):
        return 'ReportHasSubcategories with id - {}'.format(self.id)

