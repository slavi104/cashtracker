from django.test import TestCase
from app_cashtracker.helpers.ReportPDF import *
from app_cashtracker.models.User import User
from app_cashtracker.models.Category import Category
from app_cashtracker.models.Subcategory import Subcategory
from app_cashtracker.models.Payment import Payment
from app_cashtracker.models.Report import Report
from app_cashtracker.helpers.util import take_date
from django.utils import timezone


class ReportPDFTests(TestCase):

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

        report_pdf = ReportPDF(report)
        self.assertEqual(len(report_pdf.elements), 0)

        report_pdf.generate_header()
        self.assertEqual(len(report_pdf.elements), 5)

        report_pdf.generate_statistics_data_and_table()
        self.assertEqual(len(report_pdf.elements), 8)

        report_pdf.generate_pie_charts()
        self.assertEqual(len(report_pdf.elements), 9)

        if len(report_pdf.lc_data) != 0:
            report_pdf.generate_line_charts()
            self.assertEqual(len(report_pdf.elements), 10)

        report_pdf.build_and_save()

        self.assertEqual(ReportPDF.payments_table_labels, [
            'Date',
            'Name',
            'Category',
            'Subcategory',
            'Comment',
            'Value'
        ])
