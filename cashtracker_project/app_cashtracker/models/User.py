from django.db import models
from django.utils import timezone

from app_cashtracker.helpers.util import *


class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    salary = models.DecimalField(
        default=0.000,
        max_digits=19,
        decimal_places=3
    )
    currency = models.CharField(max_length=255, default="BGN")
    created = models.DateTimeField('date created')
    is_active = models.BooleanField(default=True)

    def register(self, params):
        now = timezone.now()  # + timedelta(hours=3)
        self.email = params['email']
        self.password = hash_password(params['password_1'])
        self.created = now.strftime('%Y-%m-%d %H:%M:%S')
        self.save()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
