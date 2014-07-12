import django_filters

from .models import Player


class PlayerFilter(django_filters.FilterSet):
    new_choices = (('', 'All'), ) + Player.POSITION_CHOICES
    position = django_filters.ChoiceFilter(
        lookup_type='iexact', choices=new_choices)
    first_name = django_filters.CharFilter(lookup_type='icontains')
    last_name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'position', 'birth_date',
                  'country', 'height', 'retired']
        order_by = True
