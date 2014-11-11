from django.core.exceptions import ImproperlyConfigured

from infohandball.decorators import login_required
from .models import Club


class LoveMixin(object):
    """
    Mixin to add fan status and number of fans to the context.
    """

    fan_object = None

    def get_fan_object(self):
        if self.fan_object:
            return self.fan_object
        if hasattr(self.object, 'fans'):
            return self.object
        else:
            raise ImproperlyConfigured(
                "LoveMixin requires either a definition of "
                "'fan_object' or an object that has the 'fans' attribute.")

    def is_fan(self):
        if self.request.user.is_authenticated():
            return self.get_fan_object().fans.filter(
                username=self.request.user.username).exists()
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(LoveMixin, self).get_context_data(**kwargs)
        context['fan'] = self.is_fan()
        context['fan_count'] = self.get_fan_object().fans.count()
        return context


class FavClubsMixin(object):
    """
    Mixin to add favorite clubs to the view context.
    """

    def get_context_data(self, **kwargs):
        context = super(FavClubsMixin, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['user_favs'] = Club.objects.filter(
                fans__username=self.request.user.username).values_list(
                'id', flat=True)
        return context


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class ListFilteredMixin(object):
    """
    Mixin that adds support for django-filter
    """

    filter_set = None

    def get_filter_set(self):
        if self.filter_set:
            return self.filter_set
        else:
            raise ImproperlyConfigured(
                "ListFilterMixin requires either a definition of "
                "'filter_set' or an implementation of 'get_filter()'")

    def get_filter_set_kwargs(self):
        """
        Returns the keyword arguments for instanciating the filterset.
        """
        return {
            'data': self.request.GET,
            'queryset': self.get_base_queryset(),
        }

    def get_base_queryset(self):
        """
        We can decide to either alter the queryset before or after applying the
        FilterSet
        """
        return super(ListFilteredMixin, self).get_queryset()

    def get_constructed_filter(self):
        # We need to store the instantiated FilterSet cause we use it in
        # get_queryset and in get_context_data
        if getattr(self, 'constructed_filter', None):
            return self.constructed_filter
        else:
            f = self.get_filter_set()(**self.get_filter_set_kwargs())
            self.constructed_filter = f
            return f

    def get_queryset(self):
        return self.get_constructed_filter().qs

    def get_context_data(self, **kwargs):
        kwargs.update({'filter': self.get_constructed_filter()})
        return super(ListFilteredMixin, self).get_context_data(**kwargs)
