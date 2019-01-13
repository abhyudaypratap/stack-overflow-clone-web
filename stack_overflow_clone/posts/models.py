# Third Party Stuff
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

# Stack Overflow Clone Stuff
from stack_overflow_clone.base.models import UUIDModel
from stack_overflow_clone.users.models import User


class Post(UUIDModel):
    TYPE_CHOICES = (
        ('question', "Question"),
        ('answer', "Answer"),
    )

    title = models.CharField(max_length=300)
    body = models.TextField()
    post_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_posts')
    accepted_answer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               related_name='answers', null=True, blank=True, verbose_name=_("Question"))
    score = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    last_editor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='posts_edited', null=True, blank=True)
    last_edit_date = models.DateField(_('Last Edit Date'), null=True, blank=True)
    answer_count = models.IntegerField(default=0, null=True)
    comment_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-created_on', )

    def __str__(self):
        return str(self.id)


class Comment(UUIDModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    score = models.IntegerField(default=0)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             related_name='comments', null=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ('-created_on', )

    def __str__(self):
        return str(self.id)


class Vote(UUIDModel):

    TYPE_CHOICES = (
        (1, "Upvote"),
        (2, "Downvote"),
        (3, "Favorite"),
        (4, "Accepted"),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_on = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             related_name='votes', null=True)

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        ordering = ('-created_on', )

    def __str__(self):
        return str(self.id)
