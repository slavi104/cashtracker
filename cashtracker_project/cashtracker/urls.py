from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'cashtracker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^login/', include('app_cashtracker.urls')),
    url(r'^app_cashtracker/',
        include('app_cashtracker.urls', namespace="app_cashtracker")),
    url(r'^$', include('app_cashtracker.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
