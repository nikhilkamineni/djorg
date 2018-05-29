from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # Stretch goal ideas:
    # Tags/Categories
    # Sharing notes between users
    # Hook up to bookmarks
    # File attachment
