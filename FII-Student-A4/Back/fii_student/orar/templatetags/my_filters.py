from django import template
register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def dict(Dict, key):
    return Dict[key]

@register.filter
def in_category(things, category):
    return things.filter(zi__contains=category)