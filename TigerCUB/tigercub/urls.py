from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TigerCUB.views.home', name='home'),
    # url(r'^TigerCUB/', include('TigerCUB.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'courses.views.login_user'),
    url(r'^course_picker/', 'courses.views.course_picker')
)
