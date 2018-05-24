from django.shortcuts import render
from .models import Bookmark, PersonalBookmark
# Create your views here.

def index(request):
    pbid = PersonalBookmark.objects.values_list('id')

    if request.user.is_anonymous:
        personal_bookmarks = PersonalBookmark.objects.none()
    else:
        personal_bookmarks = PersonalBookmark.objects.filter(user=request.user)

    bookmarks = Bookmark.objects.exclude(id__in=pbid)

    context = {
        'bookmarks': bookmarks,
        'personal_bookmarks': personal_bookmarks,
    }

    return render(request, 'bookmarks/index.html', context)
