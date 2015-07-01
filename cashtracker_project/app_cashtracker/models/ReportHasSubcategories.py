from django.db import models

from app_cashtracker.models import Report
from app_cashtracker.models import Subcategory
# REPORT HAS SUBCATEGORIES
class ReportHasSubcategories(models.Model):
    report = models.ForeignKey('Report')
    subcategory = models.ForeignKey('Subcategory')

    def __str__(self):
        return 'ReportHasSubcategories with id - {}'.format(self.id)

