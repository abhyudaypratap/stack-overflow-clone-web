# Third Party Stuff
from rest_framework.routers import DefaultRouter

# Stack Overflow Clone Stuff
from stack_overflow_clone.base.api.routers import SingletonRouter
from stack_overflow_clone.users.api import CurrentUserViewSet
from stack_overflow_clone.users.auth.api import AuthViewSet

default_router = DefaultRouter(trailing_slash=False)
singleton_router = SingletonRouter(trailing_slash=False)

# Register all the django rest framework viewsets below.
default_router.register('auth', AuthViewSet, basename='auth')
singleton_router.register('me', CurrentUserViewSet, basename='me')

# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls + singleton_router.urls
