from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'infohandball.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^data/', include('data.urls', namespace='data')),
    url(r'^admin/', include(admin.site.urls)),
)