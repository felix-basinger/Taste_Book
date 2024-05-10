from django import template

register = template.Library()


@register.filter(name='semicolon_to_br')
def semicolon_to_br(value):
    return value.replace(';', '<br><br>')
