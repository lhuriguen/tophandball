from datetime import datetime

from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Count, Q, Sum
from django.forms.models import modelformset_factory

from infohandball.decorators import login_required
from .models import *
from .mixins import LoveMixin, LoginRequiredMixin
from .forms import *


class ClubIndexView(generic.ListView):
    model = Club
    queryset = Club.objects.order_by('name')

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            if 'name' in self.request.GET:
                clubs = Club.objects.filter(
                    name__icontains=self.request.GET['name'])
            else:
                clubs = None
            return render_to_response(
                'data/club_search.html',
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
        if self.request.user.is_authenticated():
            context['user_favs'] = Club.objects.filter(
                fans__username=self.request.user.username).values_list(
                'id', flat=True)
        return context


class ClubDetailView(LoveMixin, generic.DetailView):
    model = Club
    #template_name = 'data/club_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubDetailView, self).get_context_data(**kwargs)
        # Prepare context data for matches
        context['comp_list'] = self.object.grouptable_set.order_by(
            'group__stage__comp_season__competition__is_international',
            'group__stage__comp_season__competition__level',
            'group__stage__order')

        return context


class ClubUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Club
    fields = ['name', 'short_name', 'initials', 'address', 'website',
              'twitter', 'facebook']
    template_name_suffix = '_update_form'


class ClubMatchView(LoveMixin, generic.ListView):
    template_name = 'data/club_matches.html'
    context_object_name = 'match_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubMatchView, self).get_context_data(**kwargs)
        context['club'] = self.object
        return context

    def get_queryset(self):
        self.object = get_object_or_404(Club, pk=self.kwargs['pk'])
        if 'a' in self.request.GET:
            return self.object.get_matches()
        else:
            return self.object.get_matches()[:5]


class ClubTeamView(LoveMixin, generic.ListView):
    template_name = 'data/club_team.html'
    context_object_name = 'staff_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubTeamView, self).get_context_data(**kwargs)
        context['club'] = self.object
        context['seasons'] = Season.objects.filter(
            playercontract__club=self.object).distinct().order_by('-year_to')

        if self.request.user.is_authenticated():
            context['user_favs'] = Player.objects.filter(
                fans__username=self.request.user.username).values_list(
                'id', flat=True)

        if 'season' in self.request.GET:
            year = self.request.GET['season']
        else:
            year = Season.curr_year()

        context['coach_list'] = CoachContract.objects.select_related(
            'coach').filter(club=self.object, season__year_from=year)

        context['scorers_list'] = Player.objects.filter(
            matchplayerstats__match_team__club=self.object,
            matchplayerstats__match_team__match__group__stage__comp_season__season__year_from=year
            ).annotate(sum_goals=Sum('matchplayerstats__goals'),
                       yellows=Sum('matchplayerstats__yellow_card'),
                       two_mins=Sum('matchplayerstats__two_minutes'),
                       reds=Sum('matchplayerstats__red_card')
                       ).order_by('-sum_goals')
        return context

    def get_queryset(self):
        self.object = get_object_or_404(Club, pk=self.kwargs['pk'])
        if 'season' in self.request.GET:
            year = self.request.GET['season']
        else:
            year = Season.curr_year()
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
                    'data/list_love.html',
                    {'item': c, 'user_favs': user_favs},
                    context_instance=RequestContext(request)
                )
            return render_to_response(
                'data/form_love.html',
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
                'data/player_search.html',
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
                'player').filter(club=ct.club,
                                 season=ct.season).exclude(pk=ct.id)
        # Matches
        matches = self.player.matchplayerstats_set.select_related().order_by(
            '-match_team__match__match_datetime')
        context['matches'] = matches  # [0:8]
        return context


class PlayerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Player
    fields = ['first_name', 'last_name', 'country', 'position', 'birth_date',
              'birth_place', 'height', 'main_hand', 'retired',
              'retirement_date']
    template_name_suffix = '_update_form'


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
                    'data/list_love.html',
                    {'item': p, 'user_favs': user_favs},
                    context_instance=RequestContext(request)
                )
            return render_to_response(
                'data/form_love.html',
                {'fan': fan, 'fan_count': p.fans.count()},
                context_instance=RequestContext(request)
            )
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('data:player_detail', kwargs={'pk': p.id}))


class ClubTeamAddView(LoginRequiredMixin, LoveMixin, generic.CreateView):
    model = PlayerContract
    form_class = PlayerContractForm
    template_name = 'data/club_team_add.html'
    club = None
    year = None

    def get_context_data(self, **kwargs):
        context = super(ClubTeamAddView,
                        self).get_context_data(**kwargs)
        context['club'] = self.club
        return context

    def get_initial(self):
        initial = super(ClubTeamAddView, self).get_initial()
        self.club = get_object_or_404(Club, pk=self.kwargs['pk'])
        self.fan_object = self.club
        initial['club'] = self.club
        if 'season' in self.request.GET:
            self.year = self.request.GET['season'] or Season.curr_year()
        else:
            self.year = Season.curr_year()
        initial['season'] = get_object_or_404(Season, year_from=self.year)
        return initial

    def get_success_url(self):
        url = reverse('data:club_team', kwargs={'pk': self.club.pk})
        return url + '?season=' + str(self.year)


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


@login_required
def club_team_edit(request, club_id):
    # Get data from url.
    c = get_object_or_404(Club, pk=club_id)
    if 'season' in request.GET:
        year = request.GET['season'] or Season.curr_year()
    else:
        year = Season.curr_year()
    s = get_object_or_404(Season, year_from=year)
    # Get contracts for club and season.
    queryset = PlayerContract.objects.filter(
        club=c, season=s)
    # Build formset.
    ContractFormSet = modelformset_factory(
        PlayerContract, form=PlayerContractForm, extra=1, can_delete=True)
    formset = ContractFormSet(request.POST or None, request.FILES or None,
                              queryset=queryset,
                              initial=[{'club': c.id, 'season': s.id}])

    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            url = reverse('data:club_team', kwargs={'pk': c.id})
            return HttpResponseRedirect(url + '?season=' + str(year))
        return render_to_response(
            'data/club_team_edit.html',
            {'formset': formset, 'club': c},
            context_instance=RequestContext(request)
        )
    else:
        return render_to_response(
            'data/club_team_edit.html',
            {'formset': formset, 'club': c},
            context_instance=RequestContext(request)
        )


class CompIndexView(generic.ListView):
    model = Competition
    context_object_name = 'comp_list'


class CompDetailView(generic.DetailView):
    model = Competition
    #template_name = 'data/comp_detail.html'

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


def index(request):
    # return HttpResponse("Hello, world. You're at the data index.")
    return render(request, 'data/index.html', None)
