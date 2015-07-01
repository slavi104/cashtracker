from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.utils import timezone

# date and time
from datetime import datetime

# json
import json

# models
from app_cashtracker.models.User import User
from app_cashtracker.models.Payment import Payment
from app_cashtracker.models.Category import Category
from app_cashtracker.models.Subcategory import Subcategory
from app_cashtracker.models.Report import Report
from app_cashtracker.models.ReportHasPayments import ReportHasPayments
from app_cashtracker.models.ReportHasCategories import ReportHasCategories
from app_cashtracker.models.ReportHasSubcategories import ReportHasSubcategories

# util functions
from app_cashtracker.helpers.util import *


def index(request):
    template = loader.get_template('app_cashtracker/index.html')
    return HttpResponse(template.render())
