from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Field, Div
from crispy_forms.bootstrap import AppendedText

from .models import UserProfile


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Your last name'

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y'], required=False,
        widget=forms.DateInput(format='%d/%m/%Y'))

    def __init__(self, *args, **kw):
        super(UserProfileForm, self).__init__(*args, **kw)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Basic Information',
                Row(
                    Field('first_name', wrapper_class='col-sm-4'),
                    Field('last_name', wrapper_class='col-sm-4'),
                )
            ),
            Fieldset(
                'Additional Information',
                Row(
                    Field('location', wrapper_class='col-sm-4'),
                    Div(
                        AppendedText('birth_date',
                                     '<i class="fa fa-calendar"></i>'),
                        css_class='col-sm-4'
                    ),
                    Field('gender', wrapper_class='col-sm-4')
                )
            )
        )

    def save(self, *args, **kwargs):
        super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()

    class Meta:
        model = UserProfile
        exclude = ('user',)
