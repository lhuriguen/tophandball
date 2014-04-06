from django.shortcuts import render
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


class PlayerIndexView(generic.ListView):
    template_name = 'data/player_index.html'
    context_object_name = 'player_list'

    def get_queryset(self):
        return Player.objects.order_by('country')


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
