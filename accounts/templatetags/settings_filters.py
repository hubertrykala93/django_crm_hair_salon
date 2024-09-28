from django.template import Library

register = Library()


@register.filter(name="cut_withdrawal_method")
def cut_withdrawal_method(value):
    return value.split(sep=" ")[0] + " " + value.split(sep=" ")[1]
