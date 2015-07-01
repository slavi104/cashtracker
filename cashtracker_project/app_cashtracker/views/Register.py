from app_cashtracker.views.General import *


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
            # request.session['user'] = user
            return HttpResponseRedirect(
                reverse('app_cashtracker:edit_profile')
            )
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
