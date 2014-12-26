from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Field, Div
from crispy_forms.bootstrap import AppendedText

from django_countries import countries

from .models import (Player, PlayerContract, PlayerName, Club, ClubName,
                     Season, Competition)
from .widgets import SingleImageInput


class BasicInlineTable(forms.ModelForm):
    """
    Base ModelForm for use as inline formset with crispy forms
    helper and table template.
    """

    def __init__(self, *args, **kwargs):
        super(BasicInlineTable, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.template = 'crispy_forms/table_inline_formset.html'


class PlayerForm(forms.ModelForm):
    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y'], required=False,
        widget=forms.DateInput(format='%d/%m/%Y'))
    retirement_date = forms.DateField(
        input_formats=['%d/%m/%Y'], required=False,
        widget=forms.DateInput(format='%d/%m/%Y'))

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'country', 'birth_date',
                  'birth_place', 'height', 'position', 'main_hand',
                  'retired', 'retirement_date', 'photo']
        widgets = {'photo': SingleImageInput(max_size=50)}

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Personal Information',
                Row(
                    Field('first_name', wrapper_class='col-sm-4'),
                    Field('last_name', wrapper_class='col-sm-4'),
                    Field('country', wrapper_class='col-sm-4')
                ),
                Row(
                    Div(
                        AppendedText('birth_date',
                                     '<i class="fa fa-calendar"></i>'),
                        css_class='col-sm-4'
                    ),
                    Field('birth_place', wrapper_class='col-sm-4'),
                    Div(AppendedText('height', 'cm'), css_class='col-sm-4')
                )
            ),
            Row(
                Div(
                    Fieldset(
                        'Playing Information',
                        Row(
                            Field('position', wrapper_class='col-sm-6'),
                            Field('main_hand', wrapper_class='col-sm-6')
                        ),
                        Row(
                            Div(Field('retired'), css_class='col-sm-6'),
                            Div(
                                AppendedText('retirement_date',
                                             '<i class="fa fa-calendar"></i>'),
                                css_class='col-sm-6'
                            ),
                        )
                    ),
                    css_class='col-sm-6'
                ),
                Div(
                    Fieldset(
                        'Profile image',
                        Field('photo', wrapper_class='col-sm-6')
                    ),
                    css_class='col-sm-6'
                )
            )
        )


class PlayerContractInline(BasicInlineTable):

    class Meta:
        model = PlayerContract
        widgets = {'photo': SingleImageInput(max_size=50)}

    def __init__(self, *args, **kwargs):
        super(PlayerContractInline, self).__init__(*args, **kwargs)
        self.helper.form_id = 'contractEditForm'


class PlayerNamesInline(BasicInlineTable):

    class Meta:
        model = PlayerName

    def __init__(self, *args, **kwargs):
        super(PlayerNamesInline, self).__init__(*args, **kwargs)
        self.helper.form_id = 'namesEditForm'


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
        self.helper.form_tag = False
        self.helper.form_id = 'teamEditForm'
        self.helper.template = 'crispy_forms/table_inline_formset.html'
        self.fields['player'].widget.attrs['class'] = 'select-player'


class ClubForm(forms.ModelForm):

    class Meta:
        model = Club
        widgets = {'logo': SingleImageInput(max_size=50)}
        exclude = ['ehf_id', 'players', 'coaches', 'fans']

    def __init__(self, *args, **kwargs):
        super(ClubForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Div(
                    Fieldset(
                        'Basic Information',
                        Row(
                            Field('name', wrapper_class='col-sm-4'),
                            Field('short_name', wrapper_class='col-sm-4'),
                            Field('initials', wrapper_class='col-sm-4'),
                        ),
                        Row(
                            Field('country', wrapper_class='col-sm-4'),
                            Field('address', wrapper_class='col-sm-8')
                        ),
                        Row(
                            Field('website', wrapper_class='col-sm-4'),
                            Field('twitter', wrapper_class='col-sm-4'),
                            Field('facebook', wrapper_class='col-sm-4')
                        ),
                    ),
                    css_class='col-sm-9'
                ),
                Div(
                    Fieldset(
                        'Profile Logo',
                        Field('logo')
                    ),
                    css_class='col-sm-3'
                )
            )
        )


class ClubNamesInline(BasicInlineTable):

    class Meta:
        model = ClubName

    def __init__(self, *args, **kwargs):
        super(ClubNamesInline, self).__init__(*args, **kwargs)
        self.helper.form_id = 'namesEditForm'


class SeasonForm(forms.Form):
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(), empty_label=None)


class BasicFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BasicFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class ClubMatchFilterForm(BasicFilterForm):
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        empty_label='All Seasons',
        required=False)
    competition = forms.ModelChoiceField(
        queryset=Competition.objects.all(),
        empty_label='All Competitions',
        required=False)
    club = forms.ModelChoiceField(
        label='Opponent',
        queryset=Club.objects.all(),
        empty_label='All Clubs',
        required=False)


class ClubFilterForm(BasicFilterForm):
    countries_empty = [('', 'All Countries')] + list(countries)

    country = forms.ChoiceField(
        choices=countries_empty,
        required=False)
    name = forms.CharField(required=False)


class PlayerFilterForm(BasicFilterForm):
    countries_empty = [('', 'All Countries')] + list(countries)
    positions_empty = [('', 'All Positions')] + list(Player.POSITION_CHOICES)

    country = forms.ChoiceField(
        choices=countries_empty, required=False)
    position = forms.MultipleChoiceField(
        label='Playing Position(s)',
        choices=Player.POSITION_CHOICES,
        required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)


# Formsets
PlayerContractFormSet = inlineformset_factory(
    Player, PlayerContract, form=PlayerContractInline,
    extra=1, can_delete=True)
PlayerNameFormSet = inlineformset_factory(
    Player, PlayerName, form=PlayerNamesInline,
    extra=1, can_delete=True)
ClubNamesFormSet = inlineformset_factory(
    Club, ClubName, form=ClubNamesInline,
    extra=1, can_delete=True)
