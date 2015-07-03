from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone

# date and time
from datetime import datetime
import time
from decimal import *
import textwrap

from app_cashtracker.helpers.util import *
import random
from collections import OrderedDict

from app_cashtracker.models.User import User
from app_cashtracker.models.Category import Category
from app_cashtracker.models.Subcategory import Subcategory

PDFS_PATH = "./app_cashtracker/static/app_cashtracker/reports/"


class Payment(models.Model):
    value = models.DecimalField(default=0.000, max_digits=19, decimal_places=3)
    currency = models.CharField(max_length=3, default="BGN")
    category = models.ForeignKey('Category')
    subcategory = models.ForeignKey('Subcategory')
    date_time = models.DateTimeField('date and time created')
    name = models.CharField(max_length=255, default="")
    comment = models.CharField(max_length=1000, default="")
    user = models.ForeignKey('User')
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

    def generate_fake_payments(user, number_payments=100):

        for payment_no in xrange(0, number_payments):
            payment = Payment()
            payment.value = random.randint(0, 80) + random.randint(0, 100)/100
            payment.currency = random.choice(
                ['BGN', 'EUR', 'USD', 'JPY', 'GBP']
            )

            payment.category = random.choice(
                Category.objects.filter(user=user, is_active=1)
            )
            payment.subcategory = random.choice(
                Subcategory.objects.filter(
                    category=payment.category,
                    is_active=True
                )
            )

            # get random date and time from 1/1/2014 to current timestamp
            # use 1425168000 for from 01/03/2015
            date_time = datetime.fromtimestamp(
                random.randint(1388534400, int(time.time()))
            ).strftime('%Y-%m-%d %H:%M:%S')

            payment.date_time = date_time
            payment.name = 'Payment {}'.format(payment_no)

            payment.comment = ' Payment Comment {} '.format(
                payment_no
            )*random.randint(0, 2)

            payment.user = user
            payment.is_active = True
            payment.save()

    def __str__(self):
        return self.name
