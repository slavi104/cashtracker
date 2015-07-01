from app_cashtracker.views.General import *

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
