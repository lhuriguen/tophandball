from django.shortcuts import render, get_object_or_404
from django.views import generic

from data.models import Club, Player, Competition


class ClubIndexView(generic.ListView):
    template_name = 'data/club_index.html'
    context_object_name = 'club_list'

    def get_queryset(self):
        return Club.objects.order_by('country')


class ClubDetailView(generic.DetailView):
    model = Club
    #template_name = 'data/club_detail.html'


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
