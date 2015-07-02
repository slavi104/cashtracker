from django.db import models


class ReportHasSubcategories(models.Model):
    report = models.ForeignKey('Report')
    subcategory = models.ForeignKey('Subcategory')

    def __str__(self):
        return 'ReportHasSubcategories with id - {}'.format(self.id)
