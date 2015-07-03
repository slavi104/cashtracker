from django.test import TestCase
from app_cashtracker.helpers.ReportPDF import *
from app_cashtracker.models.User import User
from app_cashtracker.models.Category import Category
from app_cashtracker.models.Subcategory import Subcategory
from app_cashtracker.models.Payment import Payment
from app_cashtracker.models.Report import Report
from app_cashtracker.helpers.util import take_date
from django.shortcuts import get_object_or_404
from django.utils import timezone


class ReportTests(TestCase):

    def test_create_report(self):
        now = timezone.now()
        user = User()
        user.created = now
        user.save()

        category = Category()
        category.name = 'Test category'
        category.description = ''
        category.user = user
        category.save()

        subcategory = Subcategory()
        subcategory.name = ''
        subcategory.category = category
        subcategory.save()

        payment = Payment()
        payment.value = 10
        payment.currency = 'EUR'
        payment.category = category
        payment.subcategory = subcategory
        payment.comment = ''
        payment.date_time = now
        payment.user = user
        payment.save()

        report = Report()
        report.user = user
        report.created = now.strftime('%Y-%m-%d %H:%M:%S')
        report.report_type = 'today'
        report.report_date = now.strftime('%Y-%m-%d %H:%M:%S')
        report.start_date = take_date('today')
        report.end_date = now.strftime('%Y-%m-%d %H:%M:%S')
        report.currency = 'BGN'
        report.is_active = 1
        report.save()
        report.url = 'app_cashtracker/reports/{}.pdf'.format(report)
        report.save()

        self.assertEqual(report, get_object_or_404(Report, id=report.id))
        self.assertEqual(Report.generate_report_pdf(report), report)
        self.assertEqual(report.category_names(), 'All')
        self.assertEqual(report.add_category(category), None)
        self.assertEqual(report.add_payment(payment), None)
        self.assertEqual(report.fetch_payments(), [payment])
        self.assertEqual(Report.fetch_reports(user), [report])
        self.assertEqual(
            str(report),
            'Report_from_today_in_BGN_({})'.format(report.id)
        )
