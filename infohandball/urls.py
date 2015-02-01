from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^accounts/', include('allauth.urls')),
    # Examples:
    # url(r'^$', 'infohandball.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^data/', include('data.urls', namespace='data')),
    url(r'^profile/', include('user_profile.urls', namespace='profile')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns(
    'django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
    url(r'^privacy/$', 'flatpage', {'url': '/privacy/'}, name='privacy'),
    url(r'^tos/$', 'flatpage', {'url': '/tos/'}, name='tos'),
)
