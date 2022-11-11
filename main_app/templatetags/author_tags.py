from django import template
from django.contrib.auth.models import User

from main_app.models import Task

register = template.Library()


@register.simple_tag()
def get_author():
    return User.objects.all()
