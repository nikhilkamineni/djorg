from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from .models import Note, Tag
from decouple import config


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    id = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "email", "id")


class TagSerializer(serializers.Serializer):
    name = serializers.CharField()
    color = serializers.CharField()
    created_at = serializers.DateTimeField()

    class Meta:
        model = Tag
        fields = ("name", "color", "created_at")


class NoteSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        print("VALIDATED_DATA: ", validated_data)
        # print(self.context)
        print('Trying to save note!')
        username = self.context["request"].user
        print("USERNAME: ", username)
        user_model = User.objects.get(username=username)
        print("USER_MODEL: ", user_model)

        # note = Note.objects.create(user=user, **validated_data)
        note = Note.objects.create(user=user_model, **validated_data)

        return note

    # user = UserSerializer(required=False)
    # tags = TagSerializer(many=True)

    class Meta:
        model = Note
        # fields = ("title", "content", "user", "tags")
        fields = ("title", "content")


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        print(self.request.user)
        user = self.request.user
        # import pdb; pdb.set_trace()

        # if config("DEBUG"):
        #     return Note.objects.all()
        if user.is_anonymous:
            return Note.objects.none()
        else:
            return Note.objects.filter(user=user)


class NoteTagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
