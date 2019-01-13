# Third Party Stuff
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# Stack Overflow Clone Stuff
from stack_overflow_clone.base import response
from stack_overflow_clone.users.auth.backends import UserTokenAuthentication

from . import serializers, services


class PostViewSet(viewsets.GenericViewSet):

    serializer_class = serializers.PostSerializer
    authentication_classes = (UserTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @action(methods=['POST', ], detail=False)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = services.create_post(**serializer.validated_data)
        data = serializers.PostSerializer(post).data
        return response.Created(data)
