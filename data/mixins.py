from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404

from infohandball.decorators import login_required
from .models import Club, CompetitionSeason


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


class CompSeasonMixin(object):
    model = CompetitionSeason
    context_object_name = 'comp_season'

    def get_object(self):
        queryset = self.get_queryset()
        comp_id = self.kwargs.get('comp_id', None)
        year = self.kwargs.get('year', None)
        queryset = queryset.filter(
            competition__id=comp_id, season__year_from=year)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super(CompSeasonMixin, self).get_context_data(**kwargs)
        context['competition'] = self.object.competition
        return context
