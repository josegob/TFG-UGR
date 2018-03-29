from django import template

register = template.Library()

@register.filter
def listas(lista, index):
    try:
        return lista[index]
    except IndexError:
        return ''
