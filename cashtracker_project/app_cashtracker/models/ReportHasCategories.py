from django.db import models

from app_cashtracker.models import Report
from app_cashtracker.models import Category
# REPORT HAS CATEGORIES
class ReportHasCategories(models.Model):
    report = models.ForeignKey('Report')
    category = models.ForeignKey('Category')

    def __str__(self):
        return 'ReportHasCategories with id - {}'.format(self.id)