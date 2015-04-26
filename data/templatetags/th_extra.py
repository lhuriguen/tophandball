from datetime import datetime

from django import template
from django.db.models import Count

from django_countries import countries

from data.models import Match, Player, Club

register = template.Library()


def easy_tag(func):
    """
    Decorator to facilitate template tag creation
    """

    def inner(parser, token):
        """
        Deal with the repetitive parts of parsing template tags
        """
        try:
            return func(*token.split_contents())
        except TypeError:
            raise template.TemplateSyntaxError(
                'Bad arguments for tag "%s"' % token.split_contents()[0])

    inner.__name__ = func.__name__
    inner.__doc__ = inner.__doc__
    return inner


class AppendGetNode(template.Node):

    def __init__(self, dict):
        self.dict_pairs = {}
        for pair in dict.split(','):
            pair = pair.split('=')
            self.dict_pairs[pair[0]] = template.Variable(pair[1])

    def render(self, context):
        get = context['request'].GET.copy()
        for key in self.dict_pairs:
            get[key] = self.dict_pairs[key].resolve(context)
        path = context['request'].META['PATH_INFO']
        if len(get):
            path += "?%s" % "&".join(
                ["%s=%s" % (k, v) for (k, v) in get.items() if v])
        return path


@register.tag()
@easy_tag
def append_to_get(_tag_name, dict):
    return AppendGetNode(dict)


@register.filter
def choice_display(value, arg):
    try:
        return dict(arg)[value]
    except KeyError:
        return ''


@register.filter
def to_int(value):
    return int(value)


@register.filter
def country_name(value):
    try:
        return dict(countries)[value]
    except KeyError:
        return value


@register.simple_tag
def th_icon_matches():
    return '<abbr title="Matches"><i class="fa fa-calendar"></i></abbr>'


@register.simple_tag
def th_icon_goals():
    return '<abbr title="Goals"><i class="fa fa-bullseye"></i></abbr>'


@register.simple_tag
def th_icon_saves():
    return '<abbr title="Saves"><i class="fa fa-life-ring"></i></abbr>'


@register.simple_tag
def th_icon_yellow():
    return ('<abbr title="Yellow card">'
            '<i class="fa fa-square yellow-card"></i>'
            '</abbr>')


@register.simple_tag
def th_icon_two_mins():
    return '<abbr title="Two minutes"><i class="fa fa-clock-o"></i></abbr>'


@register.simple_tag
def th_icon_red():
    return ('<abbr title="Red card">'
            '<i class="fa fa-square red-card"></i>'
            '</abbr>')


@register.inclusion_tag('data/_country_flag.html')
def th_flag(country):
    return {'country': country}


@register.inclusion_tag('data/_match_calendar.html')
def th_match_calendar():
    # We need context for upcoming and latest matches.
    upcoming = Match.objects.upcoming().select_related()[:5]
    latest = Match.objects.latest().select_related()[:5]
    return {'upcoming': upcoming, 'latest': latest}


@register.inclusion_tag('data/_birthday_list.html')
def th_birthday_list():
    m, d = datetime.now().month, datetime.now().day
    p = Player.objects.filter(
        birth_date__month=m, birth_date__day=d
        ).exclude(photo__isnull=True).exclude(
        photo__exact='').order_by('?')[:6]
    total = Player.objects.filter(
        birth_date__month=m, birth_date__day=d).count()
    return {'items': p, 'total': total}


@register.inclusion_tag('data/_popular_clubs.html')
def th_popular_clubs():
    c = Club.objects.annotate(
        num_fans=Count('fans')).filter(
        num_fans__gt=0).order_by('-num_fans')[:6]
    return {'items': c}


@register.inclusion_tag('data/_popular_players.html')
def th_popular_players():
    c = Player.objects.annotate(
        num_fans=Count('fans')).filter(
        num_fans__gt=0).order_by('-num_fans')[:6]
    return {'items': c}
