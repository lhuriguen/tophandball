from datetime import datetime

from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Count

from infohandball.decorators import login_required
from .models import Club, Player, Competition, PlayerContract
from .forms import PlayerContractFormSet, PlayerNameFormSet, PlayerForm


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class LoveMixin(object):
    """
    Mixin to add fan status and number of fans to the context.
    """

    def is_fan(self):
        if self.request.user.is_authenticated():
            return self.object.fans.filter(
                username=self.request.user.username).exists()
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(LoveMixin, self).get_context_data(**kwargs)
        context['fan'] = self.is_fan()
        context['fan_count'] = self.object.fans.count()
        return context


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
            .order_by('-num_fans')[:10]
        context['countries'] = Club.objects.values_list('country', flat=True)\
            .order_by('country').distinct()
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
    paginate_by = 125

    def get_queryset(self):
        # return Player.objects.order_by('country')
        return Player.objects.order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(PlayerIndexView, self).get_context_data(**kwargs)
        context['player_count'] = Player.objects.count()
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
        context['matches'] = matches[0:8]
        return context


class PlayerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Player
    fields = ['first_name', 'last_name', 'country', 'position', 'birth_date',
              'birth_place', 'height', 'main_hand', 'retired',
              'retirement_date']
    template_name_suffix = '_update_form'
    form_class = PlayerForm

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contract_form = PlayerContractFormSet(instance=self.object)
        names_form = PlayerNameFormSet(instance=self.object)
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
        frm = self.get_form(form_class)
        contract_frm = PlayerContractFormSet(self.request.POST)
        names_frm = PlayerNameFormSet(self.request.POST)
        if frm.is_valid() and contract_frm.is_valid() and names_frm.is_valid():
            return self.form_valid(frm, contract_frm, names_frm)
        else:
            return self.form_invalid(frm, contract_frm, names_frm)

    def form_valid(self, form, contract_form, names_form):
        """
        Called if all forms are valid. Creates a Player instance along with
        associated Contracts and Names and then redirects to a
        success page.
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
