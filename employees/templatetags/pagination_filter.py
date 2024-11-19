from django.template import Library

register = Library()


@register.simple_tag(name="url_replace")
def url_replace(request, key, value):
    dict_ = request.GET.copy()
    dict_[key] = value

    return dict_.urlencode()
