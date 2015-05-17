from django.db import models

# date and time
from datetime import datetime

# for password hashing
import uuid
import hashlib
 
# Create your models here.
# USER
class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    salary = models.FloatField(default=0.00)
    created = models.DateTimeField('date created')
    is_active = models.IntegerField(default=1)

    def register(self, params):
        self.email = params['email']
        self.password = User.hash_password(params['password_1'])
        self.created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save()

    def hash_password(password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
        
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    def __str__(self):
        return self.user_name


# PAYMENT
class Payment(models.Model):
    value = models.FloatField(default=0.00)
    currency = models.CharField(max_length=3, default="BGN")
    category = models.IntegerField()
    subcategory = models.IntegerField()
    date_time = models.DateTimeField('date and time created')
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=1000)
    user_id = models.IntegerField()
    is_active = models.IntegerField(default=1)

    def __str__(self):
        return self.name


# CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    user_id = models.IntegerField()
    is_active = models.IntegerField(default=1)

    def __str__(self):
        return self.name


# SUBCATEGORY
class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category_id = models.IntegerField()
    is_active = models.IntegerField(default=1)

    def __str__(self):
        return self.name


# REPORT
class Report(models.Model):
    user_id = models.IntegerField()
    created = models.DateTimeField('date created')
    report_type = models.CharField(max_length=255)
    report_date = models.DateTimeField('report date used for report_type')
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    currency = models.CharField(max_length=3, default="BGN")
    is_active = models.IntegerField(default=1)

    def __str__(self):
        return 'Report'


# REPORT HAS PAYMENTS
class ReportHasPayments(models.Model):
    report_id = models.IntegerField()
    payment_id = models.IntegerField()

    def __str__(self):
        return 'ReportHasPayments'


# REPORT HAS CATEGORIES
class ReportHasCategories(models.Model):
    report_id = models.IntegerField()
    category_id = models.IntegerField()

    def __str__(self):
        return 'ReportHasCategories'


# REPORT HAS SUBCATEGORIES
class ReportHasSubcategories(models.Model):
    report_id = models.IntegerField()
    subcategory_id = models.IntegerField()

    def __str__(self):
        return 'ReportHasSubcategories'

