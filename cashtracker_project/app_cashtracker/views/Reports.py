from app_cashtracker.views.General import *

def generate_report(request):

    user_id = request.session.get('user_id', False)
    params = request.POST

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    user = get_object_or_404(User, id=user_id)
    payments_for = params.get('payments_for', 'today')
    payments_curr = params.get('currency', user.currency)
    payments_cat = params.get('category', 0)

    now = timezone.now()
    report = Report()
    report.user = user
    report.created = now.strftime('%Y-%m-%d %H:%M:%S')
    report.report_type = payments_for
    report.report_date = now.strftime('%Y-%m-%d %H:%M:%S')
    report.start_date = take_date(payments_for)
    report.end_date = now.strftime('%Y-%m-%d %H:%M:%S')
    report.currency = payments_curr
    report.is_active = 1
    report.save()
    report.url = 'app_cashtracker/reports/{}.pdf'.format(report)
    report.save()

    # TODO - make it work with multiple categories
    if payments_cat and payments_cat is not '0':
        report.add_category(get_object_or_404(Category, id=payments_cat))

    payments = Payment.fetch_payments(
        payments_for, 
        payments_cat, 
        payments_curr,
        user
    )

    # add payments to report
    for payment in payments:
        report.add_payment(payment)

    report.generate_report_pdf();

    return HttpResponseRedirect(reverse('app_cashtracker:reports'))


def reports(request):

    user_id = request.session.get('user_id', False)
    params = request.POST

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))
    
    user = get_object_or_404(User, id=user_id)
    context = RequestContext(request, {
        'logged_user': user,
        'reports': Report.fetch_reports(user)

    })
    
    template = loader.get_template('app_cashtracker/reports.html')
    return HttpResponse(template.render(context))


def delete_report(request):

    user_id = request.session.get('user_id', False)

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    params = request.POST
    result = {}
    try:
        if int(params['report_id']) > 0:
            report = get_object_or_404(Report, id=int(params['report_id']))
            report.is_active = 0
            report.save()
            result['success'] = 1
    except Exception:
        result['success'] = 0
        result['message'] = 'Error in delete report'
    
    return HttpResponse(json.dumps(result, separators=(',',':')))
