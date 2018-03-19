from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    """ To avoid GET params loosing """

    query_string = request.GET.copy()
    query_string[field] = value

    return query_string.urlencode()


@register.simple_tag
def elipsis_or_number(paginator, current_page, request):
    """
    To avoid display a long page table
    """

    choosen_page = int(request.GET['page']) if 'page' in request.GET else 1

    if current_page == choosen_page:
        return choosen_page

    if current_page in (paginator.num_pages, paginator.num_pages - 1, 1, 2):
        return current_page

    if current_page in (choosen_page + 3, choosen_page - 3):
        return '...'

    if current_page in (choosen_page + 1, choosen_page + 2, choosen_page - 1, choosen_page - 2):
        return current_page
