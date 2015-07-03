from django.db import models
from django.shortcuts import get_object_or_404


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey('User')
    is_active = models.BooleanField(default=True)

    def get_category_name(category_id=0):
        if not int(category_id):
            return 'All'
        else:
            return get_object_or_404(Category, id=category_id).name

    def __str__(self):
        return self.name
