from django.template import Library

register = Library()


@register.filter(name="cut_withdrawal_method")
def cut_withdrawal_method(value):
    return value.split(sep=" ")[0] + " " + value.split(sep=" ")[1]


@register.filter(name="cut_withdrawal_method_for_url")
def cut_withdrawal_method_for_url(value):
    return value.split(sep=" ")[0].lower() + "-" + value.split(sep=" ")[1].lower()


@register.filter(name="split_invoice_status")
def split_invoice_status(value):
    return "-".join(value.split(sep=" "))


@register.filter(name="invoice_name_split")
def invoice_name_split(value):
    return value.split(sep="/")[-1]
