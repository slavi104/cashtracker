from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone

# date and time
from datetime import datetime
import time
from decimal import *
import textwrap

from .helpers.util import *
import random
from collections import OrderedDict

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
        now = timezone.now() + timedelta(hours=3)
        self.email = params['email']
        self.password = hash_password(params['password_1'])
        self.created = now.strftime('%Y-%m-%d %H:%M:%S')
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


    def generate_fake_payments(user, number_payments=100):

        for payment_no in xrange(1, number_payments):
            payment = Payment()
            payment.value = random.randint(0, 80)+random.randint(0,100)/100
            payment.currency = random.choice(['BGN','EUR','USD','JPY','GBP'])

            payment.category = random.choice(
                Category.objects.filter(user=user)
            )
            payment.subcategory = random.choice(
                Subcategory.objects.filter(category=payment.category)
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

        payments_stat_data = OrderedDict()
        payments_stat_data['all_total'] = Decimal('0')

        for payment in payments:

            payment_data = []
            # update payments objects
            orig_date = payment.date_time
            payment.parse_date(self.report_type)
            payment.convert_currency(self.currency)

            # add data for all payments
            payment_data.append(payment.date_time)
            payment_data.append(textwrap.fill(payment.name,20))
            payment_data.append(payment.category)
            payment_data.append(payment.subcategory)
            payment_data.append(textwrap.fill(payment.comment,25))
            payment_data.append(payment.value)

            # collect statistics data
            p_value = Decimal(payment.value)

            # stats for categories
            payments_stat_data['all_total'] += p_value
            category_key = 'all_category_{}'.format(payment.category.id)

            if payments_stat_data.get(category_key, 0):
                payments_stat_data[category_key] += p_value
            else:
                payments_stat_data[category_key] = p_value

            # stats for subcategories
            subcategory_key = 'all_subcategory_{}'.format(
                                                    payment.subcategory.id
                                                   )

            if payments_stat_data.get(subcategory_key, 0):
                payments_stat_data[subcategory_key] += p_value
            else:
                payments_stat_data[subcategory_key] = p_value

            # stats in time
            if self.report_type == 'month':
                date_time_key = 'date_time_{}'.format(orig_date.strftime('%U'))
            if self.report_type == 'week':
                date_time_key = 'date_time_{}'.format(orig_date.strftime('%a'))
            elif self.report_type == 'year':
                date_time_key = 'date_time_{}'.format(orig_date.strftime('%b'))
            elif self.report_type == 'beginning':
                date_time_key = 'date_time_{}'.format(orig_date.strftime('%Y'))
            elif self.report_type == 'today':
                date_time_key = 'date_time_{}'.format(orig_date.strftime('%H:%M'))

            if payments_stat_data.get(date_time_key, 0):
                payments_stat_data[date_time_key] += p_value
            else:
                payments_stat_data[date_time_key] = p_value

            payments_table.append(payment_data)
        
        elements.append(
            Paragraph(
                "Total: <b>{}{}</b><br/><br/>".format(
                    payments_stat_data['all_total'],
                    self.currency
                ),
                styleN)
            )

        # TABLE
        t=Table(payments_table, colWidths=(None, 110, None, None, 150, 50))
        t.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.25, colors.black),
            ('ALIGN', (5,1), (-1,-1), 'RIGHT')]))

        # add table to pdf
        elements.append(t)

        elements.append(PageBreak())

        elements.append(
            Paragraph(
                "<u>Charts</u><br/><br/>",
                styleH)
            )

        # pie cahrt for categories
        pc_cat = Pie()
        pc_cat.x = 0
        pc_cat.width = 160
        pc_cat.height = 160
        pc_cat.data = []
        pc_cat.labels = []
        pc_cat.sideLabels =1

        # pie chart for subcategories
        pc_subcat = Pie()
        pc_subcat.x = 250
        pc_subcat.width = 160
        pc_subcat.height = 160
        pc_subcat.data = []
        pc_subcat.labels = []
        pc_subcat.sideLabels =1
        lc_data = []
        cat_names = []

        for stat, value in payments_stat_data.items():
            stat_vars = stat.split('_');
            if stat_vars[1] == 'category':
                pc_cat.data.append(float(value))
                pc_cat.labels.append(
                    get_object_or_404(Category, id=stat_vars[2])
                )
            elif stat_vars[1] == 'subcategory':
                pc_subcat.data.append(float(value))
                pc_subcat.labels.append(
                    get_object_or_404(Subcategory, id=stat_vars[2])
                )
            elif stat_vars[1] == 'time':
                lc_data.append(float(value))
                cat_names.append(stat_vars[2])

        # PIE CHARTS IN DRAWING
        if len(pc_cat.labels) > 1:
            elements.append(
                Paragraph(
                    "<u><b>Pie charts for categories and subcategories.</b></u>",
                    styleN)
                )
            d_pie = Drawing(350, 240)
            d_pie.add(pc_cat)
            d_pie.add(pc_subcat)
            # add charts to PDF
            elements.append(d_pie)

            float_left = True
            counter = 0
            for category in pc_cat.labels:
                counter += 1
                pc_category = Pie()

                if float_left:
                    pc_category.x = 0
                    float_left = False
                else:
                    pc_category.x = 250
                    float_left = True

                pc_category.width = 160
                pc_category.height = 160
                pc_category.data = []
                pc_category.labels = []
                pc_category.sideLabels =1

                subcategories = Subcategory.objects.filter(category=category)
                
                for sc_id in list(map(lambda sc: sc.id, subcategories)):
                    # stats for subcategories
                    subcategory_key = 'all_subcategory_{}'.format(sc_id)

                    if payments_stat_data.get(subcategory_key, 0):
                        payments_stat_data[subcategory_key] += p_value
                        pc_category.data.append(float(value))
                        pc_category.labels.append(
                            get_object_or_404(Subcategory, id=sc_id)
                        )

                if counter % 2 == 0 :
                    d_pie_categories.add(pc_category)
                    elements.append(
                        Paragraph(
                            "<br/><br/><br/><u><b>Pie chart for {} and {}.</b></u>".format(
                                last_category, category),
                            styleN)
                        )
                    elements.append(d_pie_categories)
                else:
                    last_category = category
                    d_pie_categories = Drawing(350, 240)
                    d_pie_categories.add(pc_category)


        if len(lc_data) == 0:
            return self

        elements.append(
            Paragraph(
                "<br/><br/><br/><br/><br/><u><b>Line Chart for payment amounts in time.</b></u>",
                styleN)
            )

        lc = HorizontalLineChart()
        lc.x = 0
        lc.height = 150
        lc.width = 450
        lc.data = [tuple(lc_data)]
        lc.joinedLines = 1
        # catNames = 'Jan Feb Mar Apr May Jun Jul Aug'.split(' ')
        lc.categoryAxis.categoryNames = tuple(cat_names)
        lc.categoryAxis.labels.boxAnchor = 'n'
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = int(max(lc_data))
        lc.valueAxis.valueStep = int(max(lc_data)/10)
        lc.lines[0].strokeWidth = 2
        lc.lines[1].strokeWidth = 1.5

        d_lc = Drawing(350, 180)
        d_lc.add(lc)

        # add charts to PDF
        elements.append(d_lc)

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
        payments = list(map(lambda r: r.payment, rhp))
        return sorted(payments, key=lambda p: p.date_time, reverse=False)


    def __str__(self):
        return 'Report_from_{}_in_{}_{}_{}'.format(
            self.report_type, 
            self.currency, 
            self.user.id,
            'dsda'
        )


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

