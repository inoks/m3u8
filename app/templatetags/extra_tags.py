from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    """ To avoid GET params loosing """

    query_string = request.GET.copy()
    query_string[field] = value

    return query_string.urlencode()
