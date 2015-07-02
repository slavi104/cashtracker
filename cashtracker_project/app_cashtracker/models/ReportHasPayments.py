from django.db import models


class ReportHasPayments(models.Model):
    report = models.ForeignKey('Report')
    payment = models.ForeignKey('Payment')

    def __str__(self):
        return 'ReportHasPayments with id - {}'.format(self.id)
