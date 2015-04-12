from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, get_model, Avg, Max

from extra_views import ModelFormSetView

from utils.mixins import LoginRequiredMixin
from utils.decorators import (class_decorator, login_required,
                              permission_required)

from .models import *
from .mixins import (LoveMixin, FavClubsMixin,
                     CompSeasonMixin)
from .forms import *


class ClubIndexView(FavClubsMixin, generic.ListView):
    model = Club
    paginate_by = 20
    queryset = Club.objects.order_by('name')

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            if 'name' in self.request.GET:
                clubs = Club.objects.filter(
                    name__icontains=self.request.GET['name'])
            else:
                clubs = None
            return render_to_response(
                'data/_club_search.html',
                {'club_list': clubs},
                context_instance=RequestContext(self.request)
            )
        return super(ClubIndexView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(ClubIndexView, self).get_queryset()
        f = {}
        if self.request.GET.get('name'):
            f['name__icontains'] = self.request.GET['name']
        if self.request.GET.get('country'):
            f['country'] = self.request.GET['country']
        return queryset.filter(**f)

    def get_context_data(self, **kwargs):
        context = super(ClubIndexView, self).get_context_data(**kwargs)
        context['club_count'] = Club.objects.count()
        context['popular_list'] = Club.objects.annotate(
            num_fans=Count('fans')).filter(num_fans__gt=0)\
            .order_by('-num_fans')[:5]
        form = ClubFilterForm(self.request.GET or None)
        context['form'] = form
        context['club_field'] = forms.ModelChoiceField(
            queryset=Club.objects.all())
        return context


class ClubDetailView(LoveMixin, generic.DetailView):
    model = Club

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubDetailView, self).get_context_data(**kwargs)
        context['name_list'] = self.object.clubname_set.select_related(
            'season').order_by('season__year_from')
        # Prepare context data for matches
        context['comp_list'] = self.object.get_competitions()

        return context


@class_decorator(permission_required('data.change_club', raise_exception=True))
class ClubUpdateView(LoginRequiredMixin, LoveMixin, generic.UpdateView):
    model = Club
    form_class = ClubForm
    template_name_suffix = '_update_form'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        names_form = ClubNamesFormSet(
            instance=self.object, prefix='names',
            queryset=ClubName.objects.order_by('season__year_from'))
        return self.render_to_response(
            self.get_context_data(form=form, names_form=names_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        names_form = ClubNamesFormSet(
            self.request.POST, instance=self.object, prefix='names')
        if form.is_valid() and names_form.is_valid():
            return self.form_valid(form, names_form)
        else:
            return self.form_invalid(form, names_form)

    def form_valid(self, form, names_form):
        """
        Called if all forms are valid. Creates a model instance along with
        associated formset models and then redirects to a success page.
        """
        self.object = form.save()
        names_form.instance = self.object
        names_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, names_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, names_form=names_form))


class ClubMatchView(LoveMixin, generic.ListView):
    template_name = 'data/club_matches.html'
    context_object_name = 'match_list'

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            qs = self.get_queryset()
            return render_to_response(
                'data/_club_match_list.html',
                {'match_list': qs, 'club': self.object},
                context_instance=RequestContext(self.request)
            )
        return super(ClubMatchView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubMatchView, self).get_context_data(**kwargs)
        context['club'] = self.object

        form = ClubMatchFilterForm(self.request.GET or None)
        form.fields['season'].queryset = Season.objects.filter(
            competitionseason__stage__group__teams=self.object).distinct(
            ).order_by('-year_from')
        form.fields['competition'].queryset = Competition.objects.filter(
            competitionseason__stage__group__teams=self.object).distinct()
        form.fields['club'].queryset = Club.objects.exclude(pk=self.object.id)
        context['form'] = form

        return context

    def get_queryset(self):
        self.object = get_object_or_404(Club, pk=self.kwargs['pk'])
        f = {}
        if self.request.GET.get('season'):
            f['group__stage__comp_season__season_id'] = self.request.GET['season']
        if self.request.GET.get('competition'):
            f['group__stage__comp_season__competition_id'] = self.request.GET['competition']
        if self.request.GET.get('club'):
            return self.object.get_matches_with_rival(
                self.request.GET['club']).filter(**f)
        else:
            return self.object.get_matches().filter(**f)


class ClubTeamView(LoveMixin, generic.ListView):
    template_name = 'data/club_team.html'
    context_object_name = 'staff_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubTeamView, self).get_context_data(**kwargs)
        context['club'] = self.object
        context['seasons'] = Season.objects.filter(
            playercontract__club=self.object).distinct().order_by('-year_to')

        form = SeasonForm()
        form.fields['season'].queryset = Season.objects.exclude(
            playercontract__club=self.object)
        context['form'] = form

        if self.request.user.is_authenticated():
            context['user_favs'] = Player.objects.filter(
                fans__username=self.request.user.username).values_list(
                'id', flat=True)

        year = self.request.GET.get('season', '') or Season.curr_year()
        context['coach_list'] = CoachContract.objects.select_related(
            'coach').filter(club=self.object, season__year_from=year)
        context['scorers_list'] = self.object.get_scorer_list(year)
        return context

    def get_queryset(self):
        self.object = get_object_or_404(Club, pk=self.kwargs['pk'])
        year = self.request.GET.get('season', '') or Season.curr_year()
        return PlayerContract.objects.select_related(
            'player').filter(club=self.object, season__year_from=year)\
            .order_by('shirt_number')


@login_required
def club_love(request, club_id):
    c = get_object_or_404(Club, pk=club_id)
    if request.method == 'POST':
        choice = request.POST['choice']
        if choice == 'follow':
            c.fans.add(request.user)
            fan = True
        elif choice == 'unfollow':
            c.fans.remove(request.user)
            fan = False
        if request.is_ajax():
            # Template depends on location
            if request.POST['location'] == 'list':
                user_favs = Club.objects.filter(
                    fans__username=request.user.username
                ).values_list('id', flat=True)
                return render_to_response(
                    'data/_list_love.html',
                    {'item': c, 'user_favs': user_favs},
                    context_instance=RequestContext(request)
                )
            return render_to_response(
                'data/_form_love.html',
                {'fan': fan, 'fan_count': c.fans.count()},
                context_instance=RequestContext(request)
            )
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('data:club_detail', kwargs={'pk': c.id}))


class PlayerIndexView(generic.ListView):
    model = Player
    paginate_by = 40

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            if 'name' in self.request.GET:
                terms = self.request.GET['name']
                query = Q(last_name__icontains=terms) | \
                    Q(first_name__icontains=terms) | \
                    Q(playername__first_name__icontains=terms) | \
                    Q(playername__last_name__icontains=terms)
                players = Player.objects.filter(query)
            else:
                players = None
            return render_to_response(
                'data/_player_search.html',
                {'player_list': players},
                context_instance=RequestContext(self.request)
            )
        return super(PlayerIndexView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(PlayerIndexView, self).get_queryset()
        f = {}
        if self.request.GET.get('country'):
            f['country'] = self.request.GET['country']
        if self.request.GET.get('position'):
            f['position__in'] = self.request.GET.getlist('position')
        if self.request.GET.get('first_name'):
            f['first_name__icontains'] = self.request.GET['first_name']
        if self.request.GET.get('last_name'):
            f['last_name__icontains'] = self.request.GET['last_name']
        # if not 'retired' in self.request.GET:
        #     queryset = queryset.exclude(retired=True)
        return queryset.filter(**f).order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(PlayerIndexView, self).get_context_data(**kwargs)
        context['player_count'] = Player.objects.count()
        context['popular_list'] = Player.objects.annotate(
            num_fans=Count('fans')).filter(num_fans__gt=0)\
            .order_by('-num_fans')[:5]
        context['positions'] = Player.POSITION_CHOICES
        form = PlayerFilterForm(self.request.GET or None)
        context['form'] = form
        if self.request.user.is_authenticated():
            context['user_favs'] = Player.objects.filter(
                fans__username=self.request.user.username).values_list(
                'id', flat=True)
        return context


class PlayerDetailView(LoveMixin, generic.DetailView):
    model = Player

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        self.player = self.object
        context['club_career'] = self.player.playercontract_set.select_related(
            'club', 'season').order_by('-season__year_from', '-departure_month')
        # Add teammates
        ct = self.player.current_contract
        context['cur_contract'] = ct
        if ct:
            context['teammates'] = PlayerContract.objects.select_related(
                'player').filter(club=ct.club, season=ct.season
                                 ).exclude(pk=ct.id)
        # Matches
        matches = self.player.matchplayerstats_set.select_related().order_by(
            '-match__match_datetime')
        context['matches'] = matches[0:8]
        return context


@class_decorator(permission_required('data.change_player', raise_exception=True))
class PlayerUpdateView(LoginRequiredMixin, LoveMixin, generic.UpdateView):
    model = Player
    form_class = PlayerForm
    template_name_suffix = '_update_form'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contract_form = PlayerContractFormSet(
            instance=self.object, prefix='contracts',
            queryset=PlayerContract.objects.order_by('season__year_from'))
        names_form = PlayerNameFormSet(
            instance=self.object, prefix='names')
        return self.render_to_response(
            self.get_context_data(form=form,
                                  contract_form=contract_form,
                                  names_form=names_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contract_form = PlayerContractFormSet(
            self.request.POST, request.FILES,
            instance=self.object, prefix='contracts')
        names_form = PlayerNameFormSet(
            self.request.POST, instance=self.object, prefix='names')
        if (form.is_valid() and contract_form.is_valid() and
           names_form.is_valid()):
            return self.form_valid(form, contract_form, names_form)
        else:
            return self.form_invalid(form, contract_form, names_form)

    def form_valid(self, form, contract_form, names_form):
        """
        Called if all forms are valid. Creates a model instance along with
        associated formset models and then redirects to a success page.
        """
        self.object = form.save()
        contract_form.instance = self.object
        contract_form.save()
        names_form.instance = self.object
        names_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, contract_form, names_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  contract_form=contract_form,
                                  names_form=names_form))


class PlayerMatchView(LoveMixin, generic.ListView):
    template_name = 'data/player_matches.html'
    context_object_name = 'match_list'

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            qs = self.get_queryset()
            return render_to_response(
                'data/_player_match_list.html',
                {'match_list': qs, 'player': self.object},
                context_instance=RequestContext(self.request)
            )
        return super(PlayerMatchView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlayerMatchView, self).get_context_data(**kwargs)
        context['player'] = self.object

        form = PlayerMatchFilterForm(self.request.GET or None)
        form.fields['season'].queryset = Season.objects.filter(
            playercontract__player=self.object).distinct(
            ).order_by('-year_from')
        form.fields['competition'].queryset = Competition.objects.filter(
            competitionseason__stage__group__teams__playercontract__player=self.object).distinct()
        form.fields['club'].queryset = Club.objects.filter(
            playercontract__player=self.object).distinct()
        context['form'] = form

        return context

    def get_queryset(self):
        self.object = get_object_or_404(Player, pk=self.kwargs['pk'])
        f = {}
        if self.request.GET.get('season'):
            f['match__group__stage__comp_season__season_id'] = self.request.GET['season']
        if self.request.GET.get('competition'):
            f['match__group__stage__comp_season__competition_id'] = self.request.GET['competition']
        if self.request.GET.get('club'):
            f['club_id'] = self.request.GET['club']
        matches = self.object.matchplayerstats_set.select_related().order_by(
            '-match__match_datetime').filter(**f)
        return matches


@login_required
def player_love(request, player_id):
    p = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        choice = request.POST['choice']
        if choice == 'follow':
            p.fans.add(request.user)
            fan = True
        elif choice == 'unfollow':
            p.fans.remove(request.user)
            fan = False
        if request.is_ajax():
            # Template depends on location
            if request.POST['location'] == 'list':
                user_favs = Player.objects.filter(
                    fans__username=request.user.username
                ).values_list('id', flat=True)
                return render_to_response(
                    'data/_list_love.html',
                    {'item': p, 'user_favs': user_favs},
                    context_instance=RequestContext(request)
                )
            return render_to_response(
                'data/_form_love.html',
                {'fan': fan, 'fan_count': p.fans.count()},
                context_instance=RequestContext(request)
            )
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('data:player_detail', kwargs={'pk': p.id}))


from django.core import serializers


class ClubJSONView(generic.ListView):
    model = Club

    def get_queryset(self):
        base_qs = super(ClubJSONView, self).get_queryset()
        if self.request.GET.get('q'):
            return base_qs.filter(name__icontains=self.request.GET['q'])
        return base_qs

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            serializers.serialize('json', self.get_queryset()),
            content_type='application/json'
        )


class ClubAPIView(generic.DetailView):
    model = Club

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            serializers.serialize('json', [self.get_object()]),
            content_type='application/json'
        )


class PlayerJSONView(generic.ListView):
    model = Player

    def get_queryset(self):
        base_qs = super(PlayerJSONView, self).get_queryset()
        if self.request.GET.get('q'):
            words = self.request.GET['q'].split()
            queries = []
            for value in words:
                queries += [Q(first_name__icontains=value) |
                            Q(last_name__icontains=value)]
            # Take one Q object from the list
            query = queries.pop()
            # And the Q object with the ones remaining in the list
            for item in queries:
                query &= item
            return base_qs.filter(query)
        return base_qs

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            serializers.serialize('json', self.get_queryset()),
            content_type='application/json'
        )


class PlayerAPIView(generic.DetailView):
    model = Player

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            serializers.serialize('json', [self.get_object()]),
            content_type='application/json'
        )


class SearchJSONView(generic.View):

    def get_clubs(self):
        return Club.objects.filter(
            name__icontains=self.request.GET['q'])

    def get_players(self):
        words = self.request.GET['q'].split()
        queries = []
        for value in words:
            queries += [Q(first_name__icontains=value) |
                        Q(last_name__icontains=value)]
        # Take one Q object from the list
        query = queries.pop()
        # And the Q object with the ones remaining in the list
        for item in queries:
            query &= item
        return Player.objects.filter(query)

    def get_json(self):
        if self.request.GET.get('q'):
            from itertools import chain
            combined = list(chain(self.get_clubs(), self.get_players()))
            return serializers.serialize('json', combined)

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.get_json(), content_type='application/json')


@class_decorator(permission_required('data.change_playercontract', raise_exception=True))
class ClubTeamEditView(LoginRequiredMixin, LoveMixin, ModelFormSetView):
    model = PlayerContract
    form_class = PlayerContractForm
    template_name = 'data/club_team_edit.html'
    extra = 1
    can_delete = True
    club = None
    year = None

    def get_initial(self):
        initial = super(ClubTeamEditView, self).get_initial()
        season = get_object_or_404(Season, year_from=self.year)
        initial = [{'club': self.club, 'season': season}]
        return initial

    def get_context_data(self, **kwargs):
        self.fan_object = self.club
        context = super(ClubTeamEditView, self).get_context_data(**kwargs)
        context['club'] = self.club
        context['year'] = self.year
        return context

    def get_queryset(self):
        self.club = get_object_or_404(Club, pk=self.kwargs['pk'])
        if 'submit' in self.request.GET:
            season = get_object_or_404(Season, pk=self.request.GET['season'])
            self.year = season.year_from
        else:
            self.year = self.request.GET.get('season', '') or Season.curr_year()
        qs = super(ClubTeamEditView, self).get_queryset()
        return qs.filter(
            club_id=self.club, season__year_from=self.year
            ).order_by('shirt_number')

    def get_success_url(self):
        url = reverse('data:club_team', kwargs={'pk': self.club.pk})
        return url + '?season=' + str(self.year)


class CompIndexView(generic.ListView):
    model = Competition
    context_object_name = 'comp_list'

    def get_context_data(self, **kwargs):
        context = super(CompIndexView, self).get_context_data(**kwargs)
        # Upcoming and latest matches.
        context['upcoming'] = Match.objects.upcoming().select_related()[:5]
        context['latest'] = Match.objects.latest().select_related()[:5]
        context['categories'] = Category.objects.all()
        return context


class CompDetailView(generic.DetailView):
    model = Competition

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CompDetailView, self).get_context_data(**kwargs)
        context['upcoming'] = Match.objects.upcoming(
            competition=self.object).select_related()[:5]
        context['latest'] = Match.objects.latest(
            competition=self.object).select_related()[:5]
        context['club_times'] = self.object.get_participations()[:5]
        context['top_scorers'] = self.object.get_top_scorers()[:5]
        return context


class CompUpdateView(LoginRequiredMixin, generic.UpdateView):
    # UNUSED
    model = Competition
    template_name_suffix = '_update_form'
    fields = ['name', 'short_name', 'website', 'country', 'is_international',
              'level']


class CompSeasonRedirectView(generic.RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        """
        Return the url of the current or last stage for the season.
        """
        cs = get_object_or_404(CompetitionSeason,
                               competition=self.kwargs['comp_id'],
                               season__year_from=self.kwargs['year'])
        # First we try to get the current stage being played.
        last = GroupTable.objects.filter(
            group__stage__comp_season=cs).latest('group__stage__order')
        if last:
            stage = last.group.stage
        else:
            # We try the last stage by order.
            stage = Stage.objects.filter(comp_season=cs).latest('order')
        # Exit if we haven't found anything.
        if not stage:
            return None
        kwargs['pk'] = stage.id
        try:
            url = reverse('data:stage_detail', kwargs=kwargs)
        except NoReverseMatch:
            return None
        return url


class CompSeasonDetailView(FavClubsMixin, generic.DetailView):
    """
    This view has been replaced by CompSeasonRedirectView.
    """
    model = CompetitionSeason
    context_object_name = 'comp_season'
    template_name = 'data/competition_season.html'

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
        context = super(CompSeasonDetailView, self).get_context_data(**kwargs)
        context['competition'] = self.object.competition
        return context


class CompSeasonStatsView(CompSeasonMixin, generic.DetailView):
    template_name = 'data/competition_season_stats.html'

    def get_context_data(self, **kwargs):
        context = super(CompSeasonStatsView, self).get_context_data(**kwargs)
        context['player_stats'] = self.object.get_player_stats()
        max_goals = MatchPlayerStats.objects.filter(
            match__group__stage__comp_season=self.object).aggregate(
            max_goals=Max('goals'))['max_goals']
        if max_goals:
            context['max_goals_match'] = MatchPlayerStats.objects.filter(
                match__group__stage__comp_season=self.object,
                goals=max_goals).select_related('player', 'match')[0]
        m = Match.objects.filter(group__stage__comp_season=self.object)
        context['match_stats'] = m.aggregate(
            avg_home=Avg('score_home'),
            avg_away=Avg('score_away'),
            avg_spectators=Avg('spectators'))

        return context


class CompSeasonTeamsView(CompSeasonMixin, generic.DetailView):
    template_name = 'data/competition_season_teams.html'


class CompSeasonMapView(CompSeasonMixin, generic.ListView):

    def get(self, request, *args, **kwargs):
        teams = self.get_object().get_teams()
        return HttpResponse(
            serializers.serialize(
                'json', list(teams), fields=('name', 'latitude', 'longitude')),
            content_type='application/json'
        )


class StageDetailView(FavClubsMixin, generic.DetailView):
    model = Stage
    queryset = Stage.objects.all().select_related()

    def get_context_data(self, **kwargs):
        context = super(StageDetailView, self).get_context_data(**kwargs)
        context['competition'] = self.object.comp_season.competition
        context['comp_season'] = self.object.comp_season
        return context


class MatchDetailView(FavClubsMixin, generic.DetailView):
    model = Match
    queryset = Match.objects.all().select_related()

    def get_context_data(self, **kwargs):
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        context['home_stats'] = self.object.get_home_stats()
        context['away_stats'] = self.object.get_away_stats()
        self.add_all_scores(context)
        return context

    def add_all_scores(self, context):
        home = context['home_stats']
        away = context['away_stats']
        valid = self.object and home and away
        if not valid:
            return
        context['HT'] = (home.halftime_score or '?',
                         away.halftime_score or '?')
        context['ET1'] = (home.score_et1 or '-',
                          away.score_et1 or '-')
        context['ET2'] = (home.score_et2 or '-',
                          away.score_et2 or '-')
        context['7m'] = (home.score_7m or '-',
                         away.score_7m or '-')
        context['7GI'] = (home.given_7m or '-',
                          away.given_7m or '-')
        context['7GO'] = (home.goals_7m or '-',
                          away.goals_7m or '-')


@login_required
def unfollow(request):

    if request.method == 'POST':
        object_class = request.POST['object']
        object_id = request.POST['id']

        model = get_model('data', object_class)
        object = get_object_or_404(model, pk=object_id)
        object.fans.remove(request.user)

        if request.is_ajax():
            return HttpResponse(
                '{"result": "OK"}', content_type='application/json')
        # Fallback in case JavaScript is disabled.
        return HttpResponseRedirect(reverse('profile:index'))


def index(request):
    """
    Data index is just a redirect to the main index.
    """
    return HttpResponseRedirect('/')
