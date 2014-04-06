from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    # Examples:
    # url(r'^$', 'infohandball.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^data/', include('data.urls', namespace='data')),
    url(r'^admin/', include(admin.site.urls)),
)
