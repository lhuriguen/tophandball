from django.conf.urls import patterns, url

from user_profile import views


urlpatterns = patterns(
    '',
    # ex: /profile/
    url(r'^$', views.ProfileUpdateView.as_view(), name='index'),
    # ex: /profile/edit/
    url(r'^edit/$',
        views.ProfileUpdateView.as_view(), name='update'),
    )
