from django.db import models


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
