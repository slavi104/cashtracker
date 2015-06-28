from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^generate_fake_payments/(?P<number_of_payments>[0-9]+)', views.generate_fake_payments, name='generate_fake_payments'),
    url(r'^delete_report/$', views.delete_report, name='delete_report'),
    url(r'^delete_payment/$', views.delete_payment, name='delete_payment'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^payments/$', views.payments, name='payments'),
    url(r'^generate_report/$', views.generate_report, name='generate_report'),
    url(r'^add_payment/$', views.add_payment, name='add_payment'),
    url(r'^add_edit_category_action/$', views.add_edit_category_action, name='add_edit_category_action'),
    url(r'^delete_category_action/(?P<category_id>[0-9]+)', views.delete_category_action, name='delete_category_action'),
    url(r'^add_edit_category/(?P<category_id>[0-9]+)', views.add_edit_category, name='add_edit_category'),
    url(r'^edit_categories/$', views.edit_categories, name='edit_categories'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^edit_profile_action/$', views.edit_profile_action, name='edit_profile_action'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_action/$', views.login_action, name='login_action'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_action/$', views.register_action, name='register_action'),
    url(r'^home/$', views.home, name='home'),
    url(r'^$', views.index, name='index'),
]