from django import template
from user.models import Item

register = template.Library()

@register.inclusion_tag('user/latest_posts.html')
def latest_Items():
    context = {
    'l_items': Item.objects.all()[0:5]
    }
    return context