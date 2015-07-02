from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.platypus.flowables import PageBreak

from collections import OrderedDict
import textwrap
from decimal import *

from django.shortcuts import get_object_or_404
from app_cashtracker.models.Category import Category
from app_cashtracker.models.Subcategory import Subcategory

PDFS_PATH = "./app_cashtracker/static/app_cashtracker/reports/"


class ReportPDF(object):
    """Class ReportPDF create pdf file"""

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    styleH.alignment = 1
    pie_charts_w = 160
    pie_charts_h = 160
    col_widths = (None, 110, None, None, 150, 50)

    payments_table_labels = [
        'Date',
        'Name',
        'Category',
        'Subcategory',
        'Comment',
        'Value'
    ]

    def __init__(self, report):
        super(ReportPDF, self).__init__()
        # report
        self.report = report

        # container for the 'Flowable' objects
        self.elements = []

        # generate document file in PDF
        self.pdf = SimpleDocTemplate(
            "{}{}.pdf".format(PDFS_PATH, self.report),
            pagesize=letter
        )

        # all payments in report
        self.payments = self.report.fetch_payments()

        # data for statistics
        self.payments_stat_data = OrderedDict()
        self.payments_stat_data['all_total'] = Decimal('0')

        # payments table
        self.payments_table = [ReportPDF.payments_table_labels]

        # line chart data
        self.lc_data = []

        # category names
        self.cat_names = []

    def generate_header(self):
        self.elements.append(
            Paragraph(
                "<u><font color=green>PAYMENTS REPORT</font></u><br/>",
                ReportPDF.styleH)
            )

        self.elements.append(
            Paragraph(
                "by CashTracker™<br/>",
                ReportPDF.styleH)
            )

        self.elements.append(
            Paragraph(
                "<font color=green>Payments from: </font><b>{}</b>".format(
                    self.report.report_type.title()
                ),
                ReportPDF.styleN)
            )

        self.elements.append(
            Paragraph(
                "<font color=green>Currency: </font><b>{}</b>".format(
                    self.report.currency
                ),
                ReportPDF.styleN)
            )

        self.elements.append(
            Paragraph(
                "<font color=green>Categories: </font><b>{}</b>".format(
                    self.report.category_names()
                ),
                ReportPDF.styleN)
            )

    def generate_statistics_data_and_table(self):

        for payment in self.payments:

            payment_data = []
            # update payments objects
            orig_date = payment.date_time
            payment.parse_date(self.report.report_type)
            payment.convert_currency(self.report.currency)

            # add data for all payments
            payment_data.append(payment.date_time)
            payment_data.append(textwrap.fill(payment.name, 20))
            payment_data.append(payment.category)
            payment_data.append(payment.subcategory)
            payment_data.append(textwrap.fill(payment.comment, 25))
            payment_data.append(payment.value)

            # collect statistics data
            p_value = Decimal(payment.value)

            # stats for categories
            self.payments_stat_data['all_total'] += p_value
            category_key = 'all_category_{}'.format(payment.category.id)

            if self.payments_stat_data.get(category_key, 0):
                self.payments_stat_data[category_key] += p_value
            else:
                self.payments_stat_data[category_key] = p_value

            # stats for subcategories
            subcategory_key = 'all_subcategory_{}'.format(
                                                    payment.subcategory.id
                                                   )

            if self.payments_stat_data.get(subcategory_key, 0):
                self.payments_stat_data[subcategory_key] += p_value
            else:
                self.payments_stat_data[subcategory_key] = p_value

            # stats in time
            if self.report.report_type == 'month':
                date_key = 'date_time_{}'.format(orig_date.strftime('%U'))
            if self.report.report_type == 'week':
                date_key = 'date_time_{}'.format(orig_date.strftime('%a'))
            elif self.report.report_type == 'year':
                date_key = 'date_time_{}'.format(orig_date.strftime('%b'))
            elif self.report.report_type == 'beginning':
                date_key = 'date_time_{}'.format(orig_date.strftime('%Y'))
            elif self.report.report_type == 'today':
                date_key = 'date_time_{}'.format(orig_date.strftime('%H:%M'))

            if self.payments_stat_data.get(date_key, 0):
                self.payments_stat_data[date_key] += p_value
            else:
                self.payments_stat_data[date_key] = p_value

            # set data for each payments in table
            self.payments_table.append(payment_data)

        # TABLE
        table = Table(self.payments_table, colWidths=ReportPDF.col_widths)
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.green),
            ('ALIGN', (5, 1), (-1, -1), 'RIGHT'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.green)
        ]))

        # add total value
        self.elements.append(
            Paragraph(
                "<font color=green>Total: </font><b>{}{}</b><br/><br/>".format(
                    self.payments_stat_data['all_total'],
                    self.report.currency
                ),
                ReportPDF.styleN)
            )

        # add table to pdf
        self.elements.append(table)
        # new page
        self.elements.append(PageBreak())

    def generate_pie_charts(self):

        self.elements.append(
            Paragraph(
                "<u><font color=green>CHARTS</font></u><br/><br/>",
                ReportPDF.styleH)
            )

        # pie chart for categories
        pc_cat = Pie()
        pc_cat.x = 0
        pc_cat.width = ReportPDF.pie_charts_w
        pc_cat.height = ReportPDF.pie_charts_h
        pc_cat.data = []
        pc_cat.labels = []
        pc_cat.sideLabels = 1

        # pie chart for subcategories
        pc_subcat = Pie()
        pc_subcat.x = 250
        pc_subcat.width = ReportPDF.pie_charts_w
        pc_subcat.height = ReportPDF.pie_charts_h
        pc_subcat.data = []
        pc_subcat.labels = []
        pc_subcat.sideLabels = 1

        # get data for charts
        for stat, value in self.payments_stat_data.items():
            stat_vars = stat.split('_')
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
                self.lc_data.append(float(value))
                self.cat_names.append(stat_vars[2])

        # PIE CHARTS IN DRAWING
        if len(pc_cat.labels) > 1:
            self.elements.append(
                Paragraph(
                    "<u><b><font color=green>"
                    "Pie charts for categories and subcategories."
                    "</font></b></u>",
                    ReportPDF.styleN)
                )
            d_pie = Drawing(350, 240)
            d_pie.add(pc_cat)
            d_pie.add(pc_subcat)
            # add charts to PDF
            self.elements.append(d_pie)

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

            pc_category.width = ReportPDF.pie_charts_w
            pc_category.height = ReportPDF.pie_charts_h
            pc_category.data = []
            pc_category.labels = []
            pc_category.sideLabels = 1

            subcategories = Subcategory.objects.filter(category=category)

            for sc_id in list(map(lambda sc: sc.id, subcategories)):
                # stats for subcategories
                subcategory_key = 'all_subcategory_{}'.format(sc_id)

                if self.payments_stat_data.get(subcategory_key, 0):
                    # self.payments_stat_data[subcategory_key] += p_value
                    pc_category.data.append(float(value))
                    pc_category.labels.append(
                        get_object_or_404(Subcategory, id=sc_id)
                    )

            if counter % 2 == 0:
                d_pie_categories.add(pc_category)

                if len(pc_cat.labels) % 2 == 0:
                    self.elements.append(
                        Paragraph(
                            "<br/><br/><br/><u><b><font color=green>"
                            "Pie chart for {} and {}."
                            "</font></b></u>".format(
                                last_category,
                                category
                            ),
                            ReportPDF.styleN)
                        )
                    self.elements.append(d_pie_categories)
            else:
                last_category = category
                d_pie_categories = Drawing(350, 240)
                d_pie_categories.add(pc_category)

                if len(pc_cat.labels) % 2 != 0:
                    self.elements.append(
                        Paragraph(
                            "<br/><br/><br/><u><b><font color=green>"
                            "Pie chart for {}."
                            "</font></b></u>".format(category),
                            ReportPDF.styleN)
                        )
                    self.elements.append(d_pie_categories)

    def generate_line_charts(self):

        self.elements.append(
            Paragraph(
                "<br/><br/><br/><br/><br/><br/><br/><u><b><font color=green>"
                "Line Chart for payment amounts in time."
                "</font></b></u>",
                ReportPDF.styleN)
            )

        lc = HorizontalLineChart()
        lc.x = 0
        lc.height = 150
        lc.width = 450
        lc.data = [tuple(self.lc_data)]
        lc.joinedLines = 1
        lc.categoryAxis.categoryNames = tuple(self.cat_names)
        lc.categoryAxis.labels.boxAnchor = 'n'
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = int(max(self.lc_data))
        lc.valueAxis.valueStep = int(max(self.lc_data)/10)
        lc.lines[0].strokeWidth = 2
        lc.lines[1].strokeWidth = 1.5

        d_lc = Drawing(350, 180)
        d_lc.add(lc)

        # add charts to PDF
        self.elements.append(d_lc)

    def build_and_save(self):
        # write the document to disk
        self.pdf.build(self.elements)
