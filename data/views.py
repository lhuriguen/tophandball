from datetime import datetime

from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, Sum, get_model, Avg, Max

from extra_views import ModelFormSetView

from infohandball.decorators import login_required
from .models import *
from .mixins import LoveMixin, LoginRequiredMixin, FavClubsMixin
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
        if 'name' in self.request.GET:
            return queryset.filter(
                name__icontains=self.request.GET['name'])
        if 'country' in self.request.GET:
            return queryset.filter(
                country=self.request.GET['country'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ClubIndexView, self).get_context_data(**kwargs)
        context['club_count'] = Club.objects.count()
        context['popular_list'] = Club.objects.annotate(
            num_fans=Count('fans')).filter(num_fans__gt=0)\
            .order_by('-num_fans')[:5]
        context['countries'] = Club.objects.values_list('country', flat=True)\
            .order_by('country').distinct()
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
            f = {}
            if self.request.GET.get('season'):
                f['group__stage__comp_season__season_id'] = self.request.GET['season']
            if self.request.GET.get('competition'):
                f['group__stage__comp_season__competition_id'] = self.request.GET['competition']
            qs = self.get_queryset().filter(**f)
            return render_to_response(
                'data/_club_match_filter.html',
                {'match_list': qs, 'club': self.object},
                context_instance=RequestContext(self.request)
            )
        return super(ClubMatchView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubMatchView, self).get_context_data(**kwargs)
        context['club'] = self.object

        form = ClubMatchFilterForm()
        form.fields['season'].queryset = Season.objects.filter(
            competitionseason__stage__group__teams=self.object).distinct()
        form.fields['competition'].queryset = Competition.objects.filter(
            competitionseason__stage__group__teams=self.object).distinct()
        form.fields['club'].queryset = Club.objects.exclude(pk=self.object.id)
        context['form'] = form

        return context

    def get_queryset(self):
        self.object = get_object_or_404(Club, pk=self.kwargs['pk'])
        if self.request.is_ajax():
            if self.request.GET.get('club'):
                return self.object.get_matches_with_rival(
                    self.request.GET['club'])
            return self.object.get_matches()
        else:
            return self.object.get_matches()[:10]


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

        context['scorers_list'] = Player.objects.filter(
            matchplayerstats__club=self.object,
            matchplayerstats__match__group__stage__comp_season__season__year_from=year
            ).annotate(sum_goals=Sum('matchplayerstats__goals'),
                       yellows=Sum('matchplayerstats__yellow_card'),
                       two_mins=Sum('matchplayerstats__two_minutes'),
                       reds=Sum('matchplayerstats__red_card')
                       ).order_by('-sum_goals')
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
    paginate_by = 120

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
        if 'country' in self.request.GET and self.request.GET['country']:
            queryset = queryset.filter(country=self.request.GET['country'])
        if 'position' in self.request.GET and self.request.GET['position']:
            queryset = queryset.filter(position=self.request.GET['position'])
        # if not 'retired' in self.request.GET:
        #     queryset = queryset.exclude(retired=True)
        return queryset.order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(PlayerIndexView, self).get_context_data(**kwargs)
        context['player_count'] = Player.objects.count()
        context['popular_list'] = Player.objects.annotate(
            num_fans=Count('fans')).filter(num_fans__gt=0)\
            .order_by('-num_fans')[:5]
        context['countries'] = Player.objects.values_list(
            'country', flat=True).order_by('country').distinct()
        context['positions'] = Player.POSITION_CHOICES
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
            'club', 'season').order_by('-season__year_from', '-arrival_month')
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


class PlayerJSONView(generic.ListView):
    model = Player

    def get_queryset(self):
        base_qs = super(PlayerJSONView, self).get_queryset()
        if 'q' in self.request.GET:
            words = self.request.GET['q'].split()
            # Turn list of values into list of Q objects
            queries = [Q(first_name__icontains=value)
                       for value in words]
            queries += [Q(last_name__icontains=value)
                        for value in words]
            # Take one Q object from the list
            query = queries.pop()
            # Or the Q object with the ones remaining in the list
            for item in queries:
                query |= item
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
        return qs.filter(club_id=self.club, season__year_from=self.year)

    def get_success_url(self):
        url = reverse('data:club_team', kwargs={'pk': self.club.pk})
        return url + '?season=' + str(self.year)


class CompIndexView(generic.ListView):
    model = Competition
    context_object_name = 'comp_list'


class CompDetailView(generic.DetailView):
    model = Competition

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CompDetailView, self).get_context_data(**kwargs)
        # Prepare context data for latest or selected season
        year = datetime.datetime.now().year
        if 's' in self.request.GET:
            str_year = self.request.GET['s']
            if str_year.isdigit():
                year = int(str_year)
        context['comp_season'] = self.object.get_season_or_latest(year)
        return context


class CompUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Competition
    template_name_suffix = '_update_form'
    fields = ['name', 'short_name', 'website', 'country', 'is_international',
              'level']


class CompSeasonDetailView(FavClubsMixin, generic.DetailView):
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


class CompSeasonStatsView(generic.DetailView):
    model = CompetitionSeason
    context_object_name = 'comp_season'
    template_name = 'data/competition_season_stats.html'

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
        context = super(CompSeasonStatsView, self).get_context_data(**kwargs)
        context['competition'] = self.object.competition
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
    # return HttpResponse("Hello, world. You're at the data index.")
    return render(request, 'data/index.html', None)
