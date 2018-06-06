import graphene
from graphene_django import DjangoObjectType

from django.conf import settings
from .models import Note as NoteModel
from .models import Tag as TagModel
from django.contrib.auth.models import User as UserModel

class User(DjangoObjectType):
    class Meta:
        model = UserModel


class Tag(DjangoObjectType):
    class Meta:
        model = TagModel


class Note(DjangoObjectType):
    class Meta:
        model = NoteModel

        # Describe the data as a node in the graph for GraphQL
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    note = graphene.List(Note, id=graphene.String(), title=graphene.String())
    notesall = graphene.List(Note)

    def resolve_notesall(self, info):
        """Decide which notes to return"""
        user = info.context.user # Use docs or debugger to find
        if settings.DEBUG:
            return NoteModel.objects.all()
        elif user.is_anonymous:
            return NoteModel.objects.none()
        else:
            return NoteModel.objects.filter(user=user)

    def resolve_note(self, info, **kwargs):
        # title = kwargs['title'] # Exception if title does not exits
        title = kwargs.get('title')
        id = kwargs.get('id') # Returns None if the title does not exist

        if title is not None:
            return NoteModel.objects.filter(title=title)
        else:
            return NoteModel.objects.none()


class CreateNote(graphene.Mutation):
    class Arguments:
        # Input attributes for the mutation
        title = graphene.String()
        content = graphene.String()
        tags = graphene.String()

    # Output fields after mutation
    ok = graphene.Boolean()
    note = graphene.Field(Note)

    def mutate(self, info, title, content, tags):
        user = info.context.user

        if user.is_anonymous:
            is_ok = False
            return CreateNote(ok=is_ok)
        else:
            new_note = NoteModel(title=title, content=content, user=user)
            is_ok = True
            new_note.save()

            new_tags = tags.split(',')
            print(new_tags)
            for tag in new_tags:
                new_tag = TagModel.objects.get(name=tag)
                new_note.tags.add(new_tag)

            return CreateNote(note=new_note, ok=is_ok)


class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()

# Add a schema and attach the query
schema = graphene.Schema(query=Query, mutation=Mutation, types=[Note, User, Tag])

