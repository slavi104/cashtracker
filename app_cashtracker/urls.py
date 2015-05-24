from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^edit_categories/', views.edit_categories, name='edit_categories'),
    url(r'^edit_categories_action/', views.edit_categories_action, name='edit_categories_action'),
    url(r'^edit_profile/', views.edit_profile, name='edit_profile'),
    url(r'^edit_profile_action/', views.edit_profile_action, name='edit_profile_action'),
    url(r'^login/', views.login, name='login'),
    url(r'^login_action/', views.login_action, name='login_action'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^register_action/$', views.register_action, name='register_action'),
    url(r'^home/', views.home, name='home'),
    url(r'^$', views.index, name='index'),
]