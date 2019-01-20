# Third Party Stuff
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

# Stack Overflow Clone Stuff
from stack_overflow_clone.base.api.routers import SingletonRouter
from stack_overflow_clone.users.api import CurrentUserViewSet
from stack_overflow_clone.users.auth.api import AuthViewSet
from stack_overflow_clone.posts.api import PostViewSet, CommentViewSet, VoteViewSet

default_router = DefaultRouter(trailing_slash=False)
singleton_router = SingletonRouter(trailing_slash=False)

# Register all the django rest framework viewsets below.
default_router.register('auth', AuthViewSet, basename='auth')
singleton_router.register('me', CurrentUserViewSet, basename='me')

post_set = PostViewSet.as_view({
    'post': 'create',
})

update_post_set = PostViewSet.as_view({
    'get': 'get_object',
    'patch': 'partial_update',
})

comments_set = CommentViewSet.as_view({
    'get': 'get_comments',
    'post': 'create',
})

comment_set = CommentViewSet.as_view({
    'get': 'get_object',
    'patch': 'partial_update',
})

vote_set = VoteViewSet.as_view({
    'post': 'create',
})

urlpatterns_explicit = [
    url(r'^posts/$', post_set, name='posts'),
    url(r'^posts/(?P<post_id>[^/.]+)/$', update_post_set, name='posts'),
    url(r'^posts/(?P<post_id>[^/.]+)/comments/$', comments_set, name='comments'),
    url(r'^posts/(?P<post_id>[^/.]+)/comments/(?P<comment_id>[^/.]+)/$', comment_set, name='comment'),
    url(r'^posts/(?P<post_id>[^/.]+)/vote/$', vote_set, name='vote'),
]
# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls + singleton_router.urls + urlpatterns_explicit
