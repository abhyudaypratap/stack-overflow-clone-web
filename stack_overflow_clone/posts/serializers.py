from rest_framework import serializers

from . import models


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Post
        fields = ["id", "title", "body", "post_type", "owner", "accepted_answer",
                  "parent", "score", "view_count", "last_editor", "last_edit_date",
                  "answer_count", "comment_count", "favorite_count"]

    def validate(self, data):
        """
        Check that title is not empty for post type question
        """

        if data['post_type'] == "question" and not data['title']:
            raise serializers.ValidationError("Question title is required")
        return data

        if data['post_type'] == "answer" and not data['parent']:
            raise serializers.ValidationError("Question id is required for the answer")
        return data


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ["id", "post", "score", "body", "user"]


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Vote
        fields = ["id", "post", "vote_type", "user"]
