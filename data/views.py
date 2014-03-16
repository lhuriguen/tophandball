from django.shortcuts import render
from django.views import generic

from data.models import Club


class IndexView(generic.ListView):
    template_name = 'data/club_index.html'
    context_object_name = 'club_list'

    def get_queryset(self):
        return Club.objects.all()


class DetailView(generic.DetailView):
    model = Club
    #template_name = 'data/club_detail.html'


class ClubUpdateView(generic.edit.UpdateView):
    model = Club
    fields = ['name', 'short_name']
    template_name_suffix = '_update_form'


def index(request):
    #return HttpResponse("Hello, world. You're at the data index.")
    return render(request, 'data/index.html', None)
