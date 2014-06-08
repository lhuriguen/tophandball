from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from data.models import Club, Player, Competition, PlayerContract


class ClubIndexView(generic.ListView):
    template_name = 'data/club_index.html'
    context_object_name = 'club_list'

    def get_queryset(self):
        return Club.objects.order_by('country')


class ClubDetailView(generic.DetailView):
    model = Club
    #template_name = 'data/club_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubDetailView, self).get_context_data(**kwargs)
        #self.club = get_object_or_404(Club, pk=self.kwargs['pk'])
        self.club = self.object
        # Add in the fan status
        if self.request.user.is_authenticated():
            is_fan = self.request.user.fav_clubs.filter(
                id=self.club.id).exists()
            context['fan'] = is_fan
        else:
            context['fan'] = False
        # Number of fans
        context['fan_count'] = self.club.fans.count()

        # Prepare context data for matches
        context['comp_list'] = self.club.grouptable_set.order_by(
            'group__stage__comp_season__competition__is_international',
            'group__stage__comp_season__competition__level',
            'group__stage__order')

        return context


class ClubUpdateView(generic.edit.UpdateView):
    model = Club
    fields = ['name', 'short_name', 'initials', 'address', 'website',
              'twitter', 'facebook']
    template_name_suffix = '_update_form'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ClubUpdateView, self).dispatch(*args, **kwargs)


class ClubMatchView(generic.ListView):
    #model = Club
    template_name = 'data/club_matches.html'
    context_object_name = 'match_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubMatchView, self).get_context_data(**kwargs)
        # Add in the club
        context['club'] = self.club
        return context

    def get_queryset(self):
        self.club = get_object_or_404(Club, pk=self.kwargs['pk'])
        if 'a' in self.request.GET:
            return self.club.get_matches()
        else:
            return self.club.get_matches()[:5]


@login_required
def club_love(request, club_id):
    c = get_object_or_404(Club, pk=club_id)
    if request.method == 'POST':
        choice = request.POST['choice']
        if choice == 'follow':
            c.fans.add(request.user)
        elif choice == 'unfollow':
            c.fans.remove(request.user)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('data:club_detail', kwargs={'pk': c.id}))


class PlayerIndexView(generic.ListView):
    template_name = 'data/player_index.html'
    context_object_name = 'player_list'
    paginate_by = 125

    def get_queryset(self):
        # return Player.objects.order_by('country')
        return Player.objects.order_by('last_name')


class PlayerDetailView(generic.DetailView):
    model = Player

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        #self.player = get_object_or_404(Player, pk=self.kwargs['pk'])
        self.player = self.object

        # Add in the fan status
        if self.request.user.is_authenticated():
            is_fan = self.request.user.fav_players.filter(
                id=self.player.id).exists()
            context['fan'] = is_fan
        else:
            context['fan'] = False
        # Number of fans
        context['fan_count'] = self.player.fans.count()

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
        context['matches'] = matches[0:8]
        return context


@login_required
def player_love(request, player_id):
    p = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        choice = request.POST['choice']
        if choice == 'follow':
            p.fans.add(request.user)
        elif choice == 'unfollow':
            p.fans.remove(request.user)
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


def index(request):
    #return HttpResponse("Hello, world. You're at the data index.")
    return render(request, 'data/index.html', None)
