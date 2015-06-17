from django.db import models

# date and time
from datetime import datetime

from .helpers.util import *
 
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

    def __str__(self):
        return self.name


# CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)

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

    def __str__(self):
        return 'Report with id - {}'.format(self.id)


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

