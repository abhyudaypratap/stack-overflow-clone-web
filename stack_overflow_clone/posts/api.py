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

    def get_object(self, post_id):
        post = services.get_post_by_id(post_id=post_id)
        serializers_data = serializers.PostSerializer(post).data
        return serializers_data

    @action(methods=['POST', ], detail=False)
    def create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        post = services.create_post(**serializer.validated_data)
        data = serializers.PostSerializer(post).data
        return response.Created(data)

    def partial_update(self, request, post_id):
        """Update a contact"""
        data = request.data.dict()
        user = request.user
        updated_post = services.update_post(post_id=post_id, data=data, user=user)
        ser_data = serializers.PostSerializer(updated_post).data
        return response.Ok(ser_data)


class CommentViewSet(viewsets.GenericViewSet):

    serializer_class = serializers.CommentSerializer
    authentication_classes = (UserTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_comments(self, request, post_id):
        comments = services.get_all_comments(post_id=post_id)
        data = serializers.CommentSerializer(comments, many=True).data
        return response.Ok(data)

    def get_object(self, comment_id):
        comment = services.get_comment_by_id(comment_id=comment_id)
        serializers_data = serializers.CommentSerializer(comment).data
        return serializers_data

    @action(methods=['POST', ], detail=False)
    def create(self, request, post_id):
        data = request.data.dict()
        data['post'] = post_id
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        comment = services.create_comment(**serializer.validated_data)
        data = serializers.CommentSerializer(comment).data
        return response.Created(data)

    def partial_update(self, request, post_id, comment_id):
        """Update a contact"""
        instance = services.get_comment_by_id(post_id=comment_id)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Ok(serializer.data)


class VoteViewSet(viewsets.GenericViewSet):

    serializer_class = serializers.VoteSerializer
    authentication_classes = (UserTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @action(methods=['POST', ], detail=False)
    def create(self, request, post_id):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        post = services.create_vote(**serializer.validated_data)
        data = serializers.VoteSerializer(post).data
        return response.Created(data)
