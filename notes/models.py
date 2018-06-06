from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Tag(models.Model):
    # id = models.UUIDField(primary_key=True, default=int, editable=False)
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # Stretch goal ideas:
    # Tags/Categories
    # Sharing notes between users
    # Hook up to bookmarks
    # File attachment
