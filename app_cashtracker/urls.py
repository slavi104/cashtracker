from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^login_action/', views.login_action, name='login_action'),
    url(r'^register_action/$', views.register_action, name='register_action'),
    url(r'^register/', views.register, name='register'),
    url(r'^$', views.index, name='index'),
]