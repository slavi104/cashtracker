from django.db import models

# from app_cashtracker.models import Report
# from app_cashtracker.models import Payment


class ReportHasPayments(models.Model):
    report = models.ForeignKey('Report')
    payment = models.ForeignKey('Payment')

    def __str__(self):
        return 'ReportHasPayments with id - {}'.format(self.id)
