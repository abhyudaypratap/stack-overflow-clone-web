from django.db.models import F
from django.utils import timezone

# StackOverflow Stuff
from stack_overflow_clone.posts.models import Post, Comment, Vote
from stack_overflow_clone.users.models import User


def get_post_by_id(post_id):
    """
    Search user by id
    """
    post = Post.objects.filter(id=post_id).first()
    if post:
        return post
    return None


def get_comment_by_id(comment_id):
    """
    Search user by id
    """
    comment = Comment.objects.filter(id=comment_id).first()
    if comment:
        return comment
    return None


def get_all_comments(post_id):
    """
    Search user by id
    """
    comments = Comment.objects.filter(post=post_id)
    return comments


def get_vote_by_id(vote_id):
    """
    Search user by id
    """
    vote = Vote.objects.filter(id=vote_id).first()
    if vote:
        return vote
    return None


def create_post(body, post_type, owner,
                tags=None, parent=None, title=None):
    """
    Create a post
    """
    post = Post.objects.create(
        body=body,
        post_type=post_type,
        owner=owner,
        tags=tags,
        parent=parent,
        title=title
    )
    if post_type == "answer":
        Post.objects.filter(id=post.parent.id).update(answer_count=F('answer_count') + 1)
    if post_type == "question":
        User.objects.filter(id=post.owner.id).update(reputation=F('reputation') + 1)
    return post


def update_post(post_id, data, user):
    reputation = user.reputation
    instance = get_post_by_id(post_id=post_id)
    if not (user == instance.owner or reputation > 200):
        return instance
    instance = get_post_by_id(post_id=post_id)
    if data.get('body'):
        instance.body = data['body']
    if data.get('title'):
        instance.title = data['title']
    instance.last_editor = user
    instance.last_edit_date = timezone.localdate()
    instance.save()
    return instance


def create_comment(post, body, user):
    """
    Create a comment
    """
    comment = Comment.objects.create(
        post=post,
        user=user,
        body=body,
    )
    Post.objects.filter(id=comment.post.id).update(comment_count=F('comment_count') + 1)
    return comment


def create_update_vote(post, vote_type, user):
    """
    Create a vote instance
    """
    data = {'created': True, 'error': False}
    if vote_type == 1 or vote_type == 2:
        vote, created = Vote.objects.get_or_create(post=post, user=user)
        vote.vote_type = vote_type
        vote.save()
        data['created'] = created
        if vote_type == 1 and created:
            User.objects.filter(id=user.id).update(reputation=F('reputation') + 1)
        count = vote_count(vote.post.id)
        Post.objects.filter(id=vote.post.id).update(score=count)
        data['vote_count'] = count

    else:
        if vote_type == 4 and not user == post.parent.owner:
            data['message'] = "Only user asked the question can accept answer"
            data['error'] = True
            return data

        vote, created = Vote.objects.get_or_create(
            post=post,
            user=user,
            vote_type=vote_type,
        )
        data['created'] = created
        if vote_type == 3 and created:
            Post.objects.filter(id=post.id).update(favorite_count=F('favorite_count') + 1)

        elif vote_type == 4 and created:
            Post.objects.filter(id=post.parent.id).update(accepted_answer=post.answer.id)

    return data


def vote_count(post_id):
    """
    Get vote count for answer
    """
    upvote_count = Vote.objects.filter(post_id=post_id, vote_type="1").count()
    downvote_count = Vote.objects.filter(post_id=post_id, vote_type="2").count()
    vote_count = upvote_count - downvote_count
    return vote_count
