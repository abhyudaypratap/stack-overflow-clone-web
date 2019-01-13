# StackOverflow Stuff
from stack_overflow_clone.posts.models import Post


def create_post(body, post_type, owner,
                tags=None, parent=None, title=None):
    """
    Create a post if name and phone_number unique
    """
    post = Post.objects.create(
        body=body,
        post_type=post_type,
        owner=owner,
        tags=tags,
        parent=parent,
        title=title
    )
    return post


def get_post_by_id(post_id):
    """
    Search user by id
    """
    post = Post.objects.filter(id=post_id).first()
    if post:
        return post
    return None
