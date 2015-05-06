from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader

# models
from .models import User

def index(request):
    # users = User.objects.order_by('-id')
    # output = ', '.join([u.first_name for u in users])
    # return HttpResponse(output)

    template = loader.get_template('app_cashtracker/index.html')
    # context = RequestContext(request, {
    #     'users': users,
    # })
    # return HttpResponse(template.render(context))
    return HttpResponse(template.render())

def login(request):

    template = loader.get_template('app_cashtracker/login.html')
    return HttpResponse(template.render())

def register(request):

    template = loader.get_template('app_cashtracker/register.html')
    return HttpResponse(template.render())