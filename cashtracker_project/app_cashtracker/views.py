from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

# date and time
from datetime import datetime
from datetime import timedelta

# models
from .models import User
from .models import Category
from .models import Subcategory
from .models import Payment

from .helpers.util import *

import json

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
        if not check_password(user.password, password):
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
            request.session['user_id'] = user.id
            request.session['user'] = user
            return HttpResponseRedirect(reverse('app_cashtracker:edit_profile'))
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
    subcategories = {}

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    categories = Category.objects.filter(user_id=user_id, is_active=1)

    for category in categories:
        subcategories[category.id] = {}
        category_subcategories = Subcategory.objects.filter(
            category_id=category.id, 
            is_active=1
        )
        for subcategory in category_subcategories:
            subcategories[category.id][subcategory.id] = subcategory.name

    user = get_object_or_404(User, id=user_id)
    context = RequestContext(request, {
        'logged_user': user,
        'categories': categories,
        'subcategories': json.dumps(subcategories),
        'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'currency': user.currency
    })

    template = loader.get_template('app_cashtracker/home.html')
    return HttpResponse(template.render(context))


def add_payment(request):
    
    user_id = request.session.get('user_id', False)

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    params = request.POST
    payment = Payment()
    payment.value = params['value']
    payment.currency = params['currency']
    payment.category = get_object_or_404(Category, id=params['category'])
    payment.subcategory = get_object_or_404(Subcategory, 
                                            id=params['subcategory'])
    payment.date_time = params['date_time']
    payment.name = params['name']
    payment.comment = params['comment']
    payment.user = get_object_or_404(User, id=user_id)
    payment.is_active = True
    payment.save()

    return HttpResponseRedirect(reverse('app_cashtracker:home'))


def edit_profile(request):

    user_id = request.session.get('user_id', False)

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    context = RequestContext(request, {
        'logged_user': get_object_or_404(User, id=user_id)
    })
    template = loader.get_template('app_cashtracker/edit_profile.html')
    return HttpResponse(template.render(context))


def edit_profile_action(request):

    user_id = request.session.get('user_id', False)
    params = request.POST
    not_equal_passwords = False
    other_error = False

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    try:
        user = get_object_or_404(User, id=user_id)
    except Exception:
        other_error = True
        print('Error in editing profile')

    if params['password_1'] == params['password_2'] and params['password_1'] != '':
        user.password = hash_password(params['password_1'])
    elif params['password_1'] != params['password_2']:
        not_equal_passwords = True

    try:
        user.first_name = params['first_name']
        user.last_name = params['last_name']
        user.salary = params['salary']
        user.currency = params['currency']
        user.save()
    except Exception:
        other_error = True
        print('Error in editing profile')

    context = RequestContext(request, {
        'errors': {
            'not_equal_passwords': not_equal_passwords,
            'other_error': other_error
        },
        'logged_user': get_object_or_404(User, id=user_id)
    })
    
    template = loader.get_template('app_cashtracker/edit_profile.html')
    return HttpResponse(template.render(context))


def edit_categories(request):

    user_id = request.session.get('user_id', False)
    categories = Category.objects.filter(user_id=user_id, is_active=1)
    subcategories = {}

    for category in categories:
        category.subcategories = Subcategory.objects.filter(
            category_id=category.id,
            is_active=1)

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    context = RequestContext(request, {
        'logged_user': get_object_or_404(User, id=user_id),
        'categories': categories
    })

    template = loader.get_template('app_cashtracker/edit_categories.html')
    return HttpResponse(template.render(context))


def add_edit_category(request, category_id=0):

    user_id = request.session.get('user_id', False)
    params = request.POST
    other_error = False
    category = None
    subcategories = None

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    try:
        user = get_object_or_404(User, id=user_id)
        if int(category_id) > 0:
            category = get_object_or_404(Category, id=category_id)
    except Exception:
        other_error = True
        print('Error in editing category')

    if category:
        try:
            subcategories = Subcategory.objects.filter(category_id=category.id,
                is_active=1)
        except Exception:
            other_error = True
        pass

    context = RequestContext(request, {
        'errors': {
            'other_error': other_error
        },
        'logged_user': get_object_or_404(User, id=user_id),
        'category': category,
        'subcategories': subcategories
    })
    
    template = loader.get_template('app_cashtracker/add_edit_category.html')
    return HttpResponse(template.render(context))


def add_edit_category_action(request):

    user_id = request.session.get('user_id', False)
    params = request.POST
    error = False

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    if params['cat_id'] is '': # new category
        try:
            category = Category()
        except Exception:
            error = True
    else:
        try:
            category = get_object_or_404(Category, id=int(params['cat_id']))
        except Exception:
            error = True

    if not error:
        category.name = params['name']
        category.description = params['description']
        category.user_id = int(user_id)
        category.save()

        # edit old subcategories
        old_subs = Subcategory.objects.filter(category_id=category.id)
        for subcategory in old_subs:
            # if category is in post params do not delete it
            if params.dict().get('sub_{}'.format(subcategory.id), False):
                subcategory.name = params['sub_{}'.format(subcategory.id)]
                print(subcategory.name)
            else: # delete subcategory
                subcategory.is_active = 0
            subcategory.save()

        # add new subcategories
        new_subs = list(v for v in list(params.dict()) if v.startswith("new_"))
        for subcategory_key in new_subs:
            subcategory = Subcategory()
            subcategory.name = params[subcategory_key]
            subcategory.category_id = category.id
            subcategory.save()

    return HttpResponseRedirect(reverse('app_cashtracker:edit_categories'))


def delete_category_action(request, category_id=0):

    user_id = request.session.get('user_id', False)

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    try:
        if int(category_id) > 0:
            category = get_object_or_404(Category, id=int(category_id))
            category.is_active = 0
            category.save()
    except Exception:
        print('Error in delete category')
    
    return HttpResponseRedirect(reverse('app_cashtracker:edit_categories'))


def payments(request):

    user_id = request.session.get('user_id', False)

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    yesterday = datetime.now() - timedelta(hours=24)
    payments = Payment.objects.filter(
        user_id=user_id, 
        is_active=1,
        date_time__gt=yesterday.strftime('%Y-%m-%d %H:%M:%S'))

    context = RequestContext(request, {
        'logged_user': get_object_or_404(User, id=user_id),
        'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'payments': payments
    })
    
    template = loader.get_template('app_cashtracker/payments.html')
    return HttpResponse(template.render(context))
