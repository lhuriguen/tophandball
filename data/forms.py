from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Player, PlayerContract, PlayerName


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'country', 'position', 'birth_date',
                  'birth_place', 'height', 'main_hand', 'retired',
                  'retirement_date']


PlayerContractFormSet = inlineformset_factory(Player, PlayerContract, extra=4)
PlayerNameFormSet = inlineformset_factory(Player, PlayerName, extra=1)
