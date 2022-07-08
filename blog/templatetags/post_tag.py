from django import template
from blog.models import Post

register = template.Library()

@register.inclusion_tag('blog/latest_posts.html')
def latest_posts():
    context = {
    'l_posts': Post.objects.all()[0:5]
    }
    return context