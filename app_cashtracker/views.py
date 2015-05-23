from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

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
    # if this user is already logged so redirect to home page
    user_id = request.session.get('user_id', False)
    if user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:home'))

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
        else:
            request.session['user_id'] = user.id
            if request.POST.get('remember_me', False) != 'on':
                request.session.set_expiry(0) # one week

    except Exception:
        error = True

    # if this user is already logged so redirect to home page
    user_id = request.session.get('user_id', False)
    if user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:home'))

    context_vars = {
        'errors': {
            'wrong_mail_or_password': error
        },
    }

    context = RequestContext(request, context_vars)
    template = loader.get_template('app_cashtracker/login.html')
    return HttpResponse(template.render(context))


def logout(request):
    # if this user is already logged so redirect to home page
    user_id = request.session.get('user_id', False)
    if user_id:
        request.session.clear()
    
    return HttpResponseRedirect(reverse('app_cashtracker:login'))

def register(request):
    # if this user is already logged so redirect to home page
    user_id = request.session.get('user_id', False)
    if user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:home'))

    context = RequestContext(request, {
        'errors': {
            'not_equal_passwords': False
        },
    })
    template = loader.get_template('app_cashtracker/register.html')
    return HttpResponse(template.render(context))


def register_action(request):
    # if this user is already logged so redirect to home page
    user_id = request.session.get('user_id', False)
    if user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:home'))

    params = request.POST

    try:
        user = get_object_or_404(User, email=params['email'])
        existing_user = True
    except Exception:
        existing_user = False

    if params['password_1'] == params['password_2']:
        not_equal_passwords = False
        if not existing_user:
            user = User()
            user.register(params)
            return HttpResponseRedirect(reverse('app_cashtracker:login'))
    else:
        not_equal_passwords = True

    context = RequestContext(request, {
        'errors': {
            'not_equal_passwords': not_equal_passwords,
            'existing_user': existing_user
        },
    })
    
    template = loader.get_template('app_cashtracker/register.html')
    return HttpResponse(template.render(context))
    

def home(request):

    user_id = request.session.get('user_id', False)

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    context = RequestContext(request, {
        'logged_user': get_object_or_404(User, id=user_id),
    })
    template = loader.get_template('app_cashtracker/home.html')
    return HttpResponse(template.render(context))