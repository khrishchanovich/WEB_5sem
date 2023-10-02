from django import template
from mainapp.models import *

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('mainapp/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}


@register.simple_tag(name='getlets')
def get_letters(filter=None):
    if not filter:
        return Letters.objects.all()
    else:
        return Letters.objects.filter(pk=filter)


@register.inclusion_tag('mainapp/list_letters.html')
def show_letters(sort=None, let_selected=0):
    if not sort:
        lets = Letters.objects.all()
    else:
        lets = Letters.objects.order_by(sort)

    return {'lets': lets, 'let_selected': let_selected}
