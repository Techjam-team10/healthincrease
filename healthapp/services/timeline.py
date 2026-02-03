from django.db.models import F, QuerySet

from accounts.models import User
from healthapp.models import Post


def create_post(user: User, content: str) -> Post:
    return Post.objects.create(user=user, content=content)


def get_timeline_posts(limit: int | None) -> QuerySet[Post]:
    queryset = Post.objects.all()
    if limit is None:
        return queryset
    return queryset[:limit]


def increment_favorite(post: Post) -> Post:
    #F関数で競合に強く
    Post.objects.filter(pk=post.pk).update(favorite=F("favorite") + 1)
    post.refresh_from_db(fields=["favorite"])
    return post
