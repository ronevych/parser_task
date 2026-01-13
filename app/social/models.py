from django.db import models


class TimeStampedMixin(models.Model):
    """
    Mixin for implementing datetime stamps of creating and updating.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ExternalDataMixin(models.Model):
    """
    Mixin for external data.
    """

    external_id = models.BigIntegerField(unique=True, verbose_name="External ID")

    class Meta:
        abstract = True


class SocialUser(TimeStampedMixin, ExternalDataMixin):
    """
    SocialUser Model Class
    """

    username = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.username} (ext_id: {self.external_id})"

    class Meta:
        verbose_name = "Social User"
        verbose_name_plural = "Social Users"


class Post(TimeStampedMixin, ExternalDataMixin):
    """
    Post Model Class
    """

    author = models.ForeignKey(
        SocialUser, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return f"Post {self.external_id}: {self.title[:20]}..."


class Comment(TimeStampedMixin, ExternalDataMixin):
    """
    Comment Model Class
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author_email = models.EmailField(blank=True)
    body = models.TextField()

    def __str__(self):
        return f"Comment {self.external_id} on {self.post_id}"
