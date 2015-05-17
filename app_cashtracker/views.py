from django.shortcuts import get_object_or_404, render

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

    context = RequestContext(request)
    template = loader.get_template('app_cashtracker/login.html')
    return HttpResponse(template.render(context))

def login_action(request):

    error = False
    email = request.POST['email']
    password = request.POST['password']

    try:
        user = get_object_or_404(User, email=email)
        if not User.check_password(user.password, password):
            error = True
    except Exception:
        error = True

    context_vars = {
        'errors': {
            'wrong_mail_or_password': error
        },
    }

    context = RequestContext(request, context_vars)
    template = loader.get_template('app_cashtracker/login.html')
    return HttpResponse(template.render(context))

def register(request):
    context = RequestContext(request, {
        'errors': {
            'not_equal_passwords': False
        },
    })
    template = loader.get_template('app_cashtracker/register.html')
    return HttpResponse(template.render(context))

def register_action(request):

    params = request.POST

    if params['password_1'] == params['password_2']:
        user = User()
        user.register(params)
        template = loader.get_template('app_cashtracker/index.html')
        return HttpResponse(template.render())

    else:
        context = RequestContext(request, {
            'errors': {
                'not_equal_passwords': True
            },
        })
        template = loader.get_template('app_cashtracker/register.html')
        return HttpResponse(template.render(context))
    