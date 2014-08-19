from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Player, PlayerContract, PlayerName
from .widgets import SingleImageInput


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
        fields = ['club', 'season', 'player', 'shirt_number', 'photo',
                  'arrival_month', 'departure_month']
        widgets = {'club': forms.HiddenInput(),
                   'season': forms.HiddenInput(),
                   'player': forms.TextInput(),
                   'photo': SingleImageInput(max_size=50),
                   }

    def __init__(self, *args, **kwargs):
        super(PlayerContractForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'teamEditForm'
        self.helper.template = 'crispy_forms/table_inline_formset.html'
        self.helper.add_input(Submit('submit', 'Submit changes'))
        self.fields['player'].widget.attrs['class'] = 'select-player'
