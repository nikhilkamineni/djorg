import graphene
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug

from bookmarks.models import Bookmark as BookmarkModel
from bookmarks.models import PersonalBookmark as PersonalBookmarkModel
from notes.models import Note as NoteModel
from django.contrib.auth.models import User as UserModel


class User(DjangoObjectType):
    class Meta:
        model = UserModel


class Bookmark(DjangoObjectType):
    class Meta:
        model = BookmarkModel
        interfaces = (graphene.relay.Node, )


class PersonalBookmark(DjangoObjectType):
    class Meta:
        model = PersonalBookmarkModel
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    bookmark = graphene.List(Bookmark, id=graphene.String(), name=graphene.String())
    bookmarksall = graphene.List(Bookmark)
    personalbookmark = graphene.List(PersonalBookmark, id=graphene.String(), name=graphene.String())
    personalbookmarksall = graphene.List(PersonalBookmark)

    # Bookmarks
    def resolve_bookmarksall(self, info):
        return BookmarkModel.objects.all()

    def resolve_bookmark(self, info, **kwargs):
        name = kwargs.get('name')
        id = kwargs.get('id')

        if name is not None:
            return BookmarkModel.objects.filter(name=name)
        else:
            return BookmarkModel.objects.none()

    # PersonalBookmarks
    def resolve_personalbookmarksall(self, info):
        user = info.context.user
        return PersonalBookmarkModel.objects.filter(user=user)

    def resolve_personalbookmark(self, info, **kwargs):
        name = kwargs.get('name')
        id = kwargs.get('id')

        if name is not None:
            return PersonalBookmarkModel.objects.filter(name=name)
        elif id is not None:
            return PersonalBookmarkModel.objects.filter(id=id)
        else:
            return PersonalBookmarkModel.objects.none()

    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query, types=[Bookmark, PersonalBookmark, User])
