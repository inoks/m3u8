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

    if current_page == paginator.num_pages or current_page == paginator.num_pages - 1 or current_page == 1 or current_page == 2:
        return current_page

    if choosen_page + 3 == current_page or choosen_page - 3 == current_page:
        return '...'

    if choosen_page + 1 == current_page or choosen_page + 2 == current_page or choosen_page - 1 == current_page or choosen_page - 2 == current_page:
       return current_page
