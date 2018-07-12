"""djorg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from notes.api import NoteViewSet, NoteTagViewSet
from bookmarks.api import BookmarkViewSet

from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view

from graphene_django.views import GraphQLView

# def graphql_token_view():
#     view = GraphQLView.as_view(schema=schema)
#     view = permission_classes((IsAuthenticated,))(view)
#     view = authentication_classes((TokenAuthentication,))(view)
#     view = api_view['GET')](view)
#     return view

class DRFAuthenticatedGraphQLView(GraphQLView):
    def parse_body(self, request):
        if isinstance(request, rest_framework.request.Request):
            return request.data
        return super(APGraphQLView, self).parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(APGraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((IsAuthenticated,))(view)
        view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
        view = api_view(['GET', 'POST'])(view)
        return view

router = routers.DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'notetags', NoteTagViewSet)
router.register(r'bookmarks', BookmarkViewSet)

urlpatterns = [
    # path('', TemplateView.as_view(template_name='bookmarks/djorg_base.html')),
    re_path(r'^api-token-auth/', views.obtain_auth_token),
    path('', TemplateView.as_view(template_name='index.html')),
    # path('graphqltoken/', DRFAuthenticatedGraphQLView()),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('bookmarks/', include('bookmarks.urls')),
    path('notes/', include('notes.urls'))
]
