import json
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from data.models import Club, Player, Competition, Season


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
        self.club = get_object_or_404(Club, pk=self.kwargs['pk'])
        # Add in the fan status
        if self.request.user.is_authenticated():
            is_fan = self.request.user.fav_clubs.filter(id=self.club.id).exists()
            context['fan'] = is_fan
        else:
            context['fan'] = False
        # Number of fans
        context['fan_count'] = self.club.fans.count()

        # Prepare context data for matches
        s = Season.objects.get(year_to=datetime.now().year)
        context['comp_list'] = self.club.group_set.filter(
            stage__comp_season__season=s).order_by(
            'stage__comp_season__competition__is_international',
            '-stage__comp_season__competition__level')

        return context


class ClubUpdateView(generic.edit.UpdateView):
    model = Club
    fields = ['name', 'short_name']
    template_name_suffix = '_update_form'


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
        # Handle view with or without AJAX
        if request.is_ajax():
            new_count = c.fans.count()
            return HttpResponse(json.dumps({'fan_count': new_count}), mimetype="application/json")
        else:
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('data:club_detail', kwargs={'pk': c.id}))


class PlayerIndexView(generic.ListView):
    template_name = 'data/player_index.html'
    context_object_name = 'player_list'
    paginate_by = 125

    def get_queryset(self):
        # return Player.objects.order_by('country')
        return Player.objects.order_by('last_name')


class PlayerDetailView(generic.DetailView):
    model = Player


class CompIndexView(generic.ListView):
    template_name = 'data/comp_index.html'
    context_object_name = 'comp_list'

    def get_queryset(self):
        return Competition.objects.all()


class CompDetailView(generic.DetailView):
    model = Competition
    template_name = 'data/comp_detail.html'


def index(request):
    #return HttpResponse("Hello, world. You're at the data index.")
    return render(request, 'data/index.html', None)
