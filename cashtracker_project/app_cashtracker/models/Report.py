from django.db import models
from django.utils import timezone

# date and time
from datetime import datetime
import time
import random

from app_cashtracker.models.User import User
from app_cashtracker.models.Payment import Payment
from app_cashtracker.models.Category import Category
from app_cashtracker.models.Subcategory import Subcategory
from app_cashtracker.models.ReportHasPayments import ReportHasPayments
from app_cashtracker.models.ReportHasCategories import ReportHasCategories

from app_cashtracker.helpers.util import *
from app_cashtracker.helpers.ReportPDF import *


class Report(models.Model):
    user = models.ForeignKey('User')
    created = models.DateTimeField('date created')
    report_type = models.CharField(max_length=255)
    report_date = models.DateTimeField('report date used for report_type')
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    currency = models.CharField(max_length=3, default="BGN")
    url = models.CharField(max_length=255, default="")
    is_active = models.BooleanField(default=True)

    def generate_report_pdf(self):
        report_pdf = ReportPDF(self)
        report_pdf.generate_header()
        report_pdf.generate_statistics_data_and_table()
        report_pdf.generate_pie_charts()

        if len(report_pdf.lc_data) != 0:
            report_pdf.generate_line_charts()

        report_pdf.build_and_save()
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
        payments = list(map(lambda r: r.payment, rhp))
        return sorted(payments, key=lambda p: p.date_time, reverse=False)

    def fetch_reports(user):
        reports = Report.objects.filter(
            user=user,
            is_active=1).order_by('-created')
        return list(map(lambda r: r.parse_date(), reports))

    def parse_date(self):
        self.created = self.created.strftime('%d/%m/%Y')
        return self

    def __str__(self):
        return 'Report_from_{}_in_{}_({})'.format(
            self.report_type,
            self.currency,
            self.id
        )
