from django.db import models


class ReportHasCategories(models.Model):
    report = models.ForeignKey('Report')
    category = models.ForeignKey('Category')

    def __str__(self):
        return 'ReportHasCategories with id - {}'.format(self.id)
