from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

# models
from .models import User
from .models import Category
from .models import Subcategory

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
            request.session['user_id'] = user.id
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

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    context = RequestContext(request, {
        'logged_user': get_object_or_404(User, id=user_id),
        'categories': Category.objects.filter(user_id=user_id)
    })
    template = loader.get_template('app_cashtracker/home.html')
    return HttpResponse(template.render(context))


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
        user.password = User.hash_password(params['password_1'])
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
    categories = Category.objects.filter(user_id=user_id)
    subcategories = {}

    for category in categories:
        category.subcategories = Subcategory.objects.filter(category_id=category.id)

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    context = RequestContext(request, {
        'logged_user': get_object_or_404(User, id=user_id),
        'categories': categories
    })

    print(categories)
    print(subcategories)

    template = loader.get_template('app_cashtracker/edit_categories.html')
    return HttpResponse(template.render(context))


def add_edit_category(request, category_id=0):

    user_id = request.session.get('user_id', False)
    params = request.POST
    other_error = False

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    try:
        user = get_object_or_404(User, id=user_id)
    except Exception:
        other_error = True
        print('Error in editing profile')

    context = RequestContext(request, {
        'errors': {
            'other_error': other_error
        },
        'logged_user': get_object_or_404(User, id=user_id)
    })
    
    template = loader.get_template('app_cashtracker/add_edit_category.html')
    return HttpResponse(template.render(context))


def add_edit_category_action(request):

    user_id = request.session.get('user_id', False)
    params = request.POST
    other_error = False

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    try:
        user = get_object_or_404(User, id=user_id)
    except Exception:
        other_error = True
        print('Error in editing profile')

    context = RequestContext(request, {
        'errors': {
            'other_error': other_error
        },
        'logged_user': get_object_or_404(User, id=user_id)
    })
    
    template = loader.get_template('app_cashtracker/edit_categories.html')
    return HttpResponse(template.render(context))


def delete_category_action(request, category_id=0):

    user_id = request.session.get('user_id', False)
    params = request.POST
    other_error = False

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    try:
        user = get_object_or_404(User, id=user_id)
    except Exception:
        other_error = True
        print('Error in editing profile')

    context = RequestContext(request, {
        'errors': {
            'other_error': other_error
        },
        'logged_user': get_object_or_404(User, id=user_id)
    })
    
    template = loader.get_template('app_cashtracker/edit_categories.html')
    return HttpResponse(template.render(context))