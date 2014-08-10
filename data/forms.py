from django import forms
from django.forms.models import inlineformset_factory

from .models import Player, PlayerContract, PlayerName


class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'country', 'position',
                  'birth_date', 'birth_place', 'height', 'main_hand',
                  'retired', 'retirement_date']


PlayerContractFormSet = inlineformset_factory(Player, PlayerContract, extra=4)
PlayerNameFormSet = inlineformset_factory(Player, PlayerName, extra=1)


class PlayerContractForm(forms.ModelForm):

    class Meta:
        model = PlayerContract
        fields = ['club', 'season', 'player', 'shirt_number',
                  'arrival_month', 'departure_month', 'photo']
        widgets = {'club': forms.HiddenInput(),
                   'season': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(PlayerContractForm, self).__init__(*args, **kwargs)
        self.fields['player'].widget.attrs['class'] = 'selectable'
