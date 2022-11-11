from django.contrib.auth.models import User
from django.db import models
from django.db.models import *
from django.urls import reverse


class Task(Model):
    author = ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    title = CharField(max_length=100)
    text = TextField()
    image = ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'task', kwargs={
                'pk': self.pk
            }
        )
