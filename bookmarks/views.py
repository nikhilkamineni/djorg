from django.shortcuts import render
from .models import Bookmark, PersonalBookmark
from .forms import BookmarkForm

def index(request):
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            # TODO check for request.user to allow for personal bookmarks
            form.save()
        else:
            #TODO error
            pass

    pbid = PersonalBookmark.objects.values_list('id')

    if request.user.is_anonymous:
        personal_bookmarks = PersonalBookmark.objects.none()
    else:
        personal_bookmarks = PersonalBookmark.objects.filter(user=request.user)

    bookmarks = Bookmark.objects.exclude(id__in=pbid)

    context = {
        'bookmarks': bookmarks,
        'personal_bookmarks': personal_bookmarks,
        'form': BookmarkForm
    }

    return render(request, 'bookmarks/index.html', context)
