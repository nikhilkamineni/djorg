from django.shortcuts import render
from .models import Bookmark
# Create your views here.

def index(request):
    bookmarks = Bookmark.objects.all()
    context = {
        'bookmarks': bookmarks
    }

    return render(request, 'bookmarks/index.html', context)
