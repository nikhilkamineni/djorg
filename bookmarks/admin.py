from django.contrib import admin

from .models import Bookmark, PersonalBookmark

admin.site.register((Bookmark, PersonalBookmark))
