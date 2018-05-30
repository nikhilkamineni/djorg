from rest_framework import serializers, viewsets
from .models import Bookmark, PersonalBookmark

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user

        bookmark = Bookmark.objects.create(user=user, **validated_data)

        return bookmark

    class Meta:
        model = Bookmark
        fields = ('url', 'name', 'notes')


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
