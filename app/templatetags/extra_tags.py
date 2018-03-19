from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    """ To avoid GET params loosing """

    query_string = request.GET.copy()
    query_string[field] = value

    return query_string.urlencode()


@register.simple_tag
def ellipsis_or_number(paginator, current_page, request):
    """
    To avoid display a long page table
    """

    chosen_page = int(request.GET['page']) if 'page' in request.GET else 1

    if current_page == chosen_page:
        return chosen_page

    if current_page in (chosen_page + 3, chosen_page - 3):
        return '...'

    if current_page in (chosen_page + 1, chosen_page + 2, chosen_page - 1,
                        chosen_page - 2, paginator.num_pages, paginator.num_pages - 1, 1, 2):
        return current_page
