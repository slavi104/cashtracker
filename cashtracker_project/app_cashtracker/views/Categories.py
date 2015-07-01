from app_cashtracker.views.General import *

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


