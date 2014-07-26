from datetime import datetime

from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Count, Q, Avg, Sum

from infohandball.decorators import login_required
from .models import *
from .mixins import LoveMixin, LoginRequiredMixin


class ClubIndexView(generic.ListView):
    template_name = 'data/club_index.html'
    context_object_name = 'club_list'

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
        if 'name' in self.request.GET:
            return Club.objects.filter(
                name__icontains=self.request.GET['name']).order_by('name')
        if 'country' in self.request.GET:
            return Club.objects.filter(
                country=self.request.GET['country']).order_by('name')
        return Club.objects.order_by('name')

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
        self.club = self.object
        # Prepare context data for matches
        context['comp_list'] = self.club.grouptable_set.order_by(
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
    #model = Club
    template_name = 'data/club_matches.html'
    context_object_name = 'match_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubMatchView, self).get_context_data(**kwargs)
        # Add in the club
        context['club'] = self.object
        return context

    def get_queryset(self):
        self.object = get_object_or_404(Club, pk=self.kwargs['pk'])
        if 'a' in self.request.GET:
            return self.object.get_matches()
        else:
            return self.object.get_matches()[:5]


class ClubTeamView(LoveMixin, generic.ListView):
    #model = Club
    template_name = 'data/club_team.html'
    context_object_name = 'staff_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubTeamView, self).get_context_data(**kwargs)
        # Add in the club
        context['club'] = self.object
        context['seasons'] = Season.objects.filter(
            playercontract__club=self.object).distinct()

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
            return PlayerContract.objects.select_related(
                'player').filter(club=self.object, season__year_from=year)\
                .order_by('shirt_number')
        return self.object.get_current_team().order_by('shirt_number')


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
    template_name = 'data/player_index.html'
    context_object_name = 'player_list'
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
        query = Player.objects.all()
        if 'country' in self.request.GET and self.request.GET['country']:
            query = query.filter(country=self.request.GET['country'])
        if 'position' in self.request.GET and self.request.GET['position']:
            query = query.filter(position=self.request.GET['position'])
        # if not 'retired' in self.request.GET:
        #     query = query.exclude(retired=True)
        return query.order_by('last_name')

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
            'club', 'season').all()
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
        context['matches'] = matches #[0:8]
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


class CompIndexView(generic.ListView):
    template_name = 'data/comp_index.html'
    context_object_name = 'comp_list'

    def get_queryset(self):
        return Competition.objects.all()


class CompDetailView(generic.DetailView):
    model = Competition
    template_name = 'data/comp_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CompDetailView, self).get_context_data(**kwargs)
        self.competition = get_object_or_404(Competition, pk=self.kwargs['pk'])
        # Prepare context data for latest or selected season
        year = datetime.now().year
        if 's' in self.request.GET:
            str_year = self.request.GET['s']
            if str_year.isdigit():
                year = int(str_year)
        context['comp_season'] = self.competition.get_season_or_latest(year)
        return context


class CompUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Competition
    template_name_suffix = '_update_form'
    fields = ['name', 'short_name', 'website', 'country', 'is_international',
              'level']


def index(request):
    # return HttpResponse("Hello, world. You're at the data index.")
    return render(request, 'data/index.html', None)
