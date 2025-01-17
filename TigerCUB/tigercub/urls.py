from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tigercub.views.home', name='home'),
    # url(r'^tigercub/', include('tigercub.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'courses.views.login_user'),
    url(r'^logout/', 'courses.views.logout_user'),
    url(r'^results/', 'courses.views.results'),
)
