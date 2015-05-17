from django import template

register = template.Library()


@register.filter
def full_url(url, request):
    """
        Receives a relative url and returns the same url with all
        the necessary path information to be used offsite.
    """
    return request.build_absolute_uri(url)
