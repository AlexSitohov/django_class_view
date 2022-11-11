from django.contrib.admin import *

from main_app.models import Task


# Register your models here.
@register(Task)
class TaskAdmin(ModelAdmin):
    pass
