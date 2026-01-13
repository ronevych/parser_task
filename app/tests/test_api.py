import pytest

from social.models import Comment, Post, SocialUser


@pytest.mark.django_db
def test_get_users_list(api_client):
    """
    Перевіряємо список юзерів.
    """
    SocialUser.objects.create(external_id=1, username="u1", email="u1@test.com")
    SocialUser.objects.create(external_id=2, username="u2", email="u2@test.com")

    response = api_client.get("/api/users/")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 2


@pytest.mark.django_db
def test_posts_list_structure(api_client):
    """
    Перевіряємо структуру поста (Nested Author).
    """
    u = SocialUser.objects.create(external_id=1, username="author_x", email="x@x.com")
    Post.objects.create(external_id=10, title="My Title", author=u)

    response = api_client.get("/api/posts/")
    data = response.json()["results"][0]

    assert data["title"] == "My Title"
    assert data["author"]["username"] == "author_x"


@pytest.mark.django_db
def test_comments_filtering(api_client):
    """
    Перевіряємо фільтрацію коментарів по post_id.
    """
    u = SocialUser.objects.create(external_id=1, username="u", email="e")
    p1 = Post.objects.create(external_id=10, title="P1", author=u)
    p2 = Post.objects.create(external_id=20, title="P2", author=u)

    Comment.objects.create(external_id=1, body="Comment for P1", post=p1)
    Comment.objects.create(external_id=2, body="Comment for P2", post=p2)

    response = api_client.get(f"/api/comments/?post={p1.id}")

    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 1
    assert results[0]["body"] == "Comment for P1"
