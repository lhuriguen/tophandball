from django.views import generic
from django.core.urlresolvers import reverse

from utils.mixins import LoginRequiredMixin

from .models import UserProfile
from .forms import UserProfileForm


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserProfile

    def get_object(self):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile/profile_form.html'

    def get_object(self):
        """
        Returns the request's user profile.
        """
        return self.request.user.profile

    def get_success_url(self):
        return reverse('profile:index')
