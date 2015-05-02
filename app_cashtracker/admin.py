from django.contrib import admin

# Register your models here.
from .models import User
from .models import Payment
from .models import Category
from .models import Subcategory
from .models import Report
from .models import ReportHasPayments
from .models import ReportHasCategories
from .models import ReportHasSubcategories

admin.site.register(User)
admin.site.register(Payment)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Report)
admin.site.register(ReportHasPayments)
admin.site.register(ReportHasCategories)
admin.site.register(ReportHasSubcategories)