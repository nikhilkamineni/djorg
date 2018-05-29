from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    url = models.URLField('URL', unique=True)
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class PersonalBookmark(Bookmark):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
