from django.contrib import admin

# Register your models here.
from .models.User import User
from .models.Payment import Payment
from .models.Category import Category
from .models.Subcategory import Subcategory
from .models.Report import Report
from .models.ReportHasPayments import ReportHasPayments
from .models.ReportHasCategories import ReportHasCategories
from .models.ReportHasSubcategories import ReportHasSubcategories

admin.site.register(User)
admin.site.register(Payment)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Report)
admin.site.register(ReportHasPayments)
admin.site.register(ReportHasCategories)
admin.site.register(ReportHasSubcategories)
