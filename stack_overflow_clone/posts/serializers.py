from rest_framework import serializers

from . import models


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Post
        fields = ['id', "title", "body", "post_type", "owner", "accepted_answer",
                  "parent", "score", "view_count", "last_editor", "last_edit_date",
                  "answer_count", "comment_count", "favorite_count", "tags"]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ["id", "post", "score", "body", "user"]


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Vote
        fields = ["id", "post", "vote_type", "user"]
