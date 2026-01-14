import pytest

from social.models import Comment, Post, SocialUser
from social.services import fetch_comments, fetch_posts, fetch_users


@pytest.mark.django_db
def test_fetch_users_success(requests_mock):
    """
    Перевіряємо, що юзери зберігаються коректно.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    requests_mock.get(
        url,
        json=[
            {
                "id": 1,
                "username": "TestUser",
                "email": "test@example.com",
                "name": "Test Name",
            }
        ],
        status_code=200,
    )

    fetch_users()

    assert SocialUser.objects.count() == 1
    user = SocialUser.objects.get(external_id=1)
    assert user.username == "TestUser"


@pytest.mark.django_db
def test_fetch_posts_strict_consistency(requests_mock):
    """
    Strict Mode Check
    If No Author in DB, then Post being ignored
    """
    user = SocialUser.objects.create(
        external_id=10, username="our_user", email="me@test.com"
    )

    mock_posts = [
        {"id": 100, "title": "Good Post", "body": "...", "userId": 10},
        {"id": 101, "title": "Bad Post", "body": "...", "userId": 999},
    ]

    url = "https://dummyjson.com/posts"
    requests_mock.get(url, json={"posts": mock_posts}, status_code=200)

    fetch_posts()

    assert Post.objects.count() == 1
    saved_post = Post.objects.first()
    assert saved_post.external_id == 100
    assert saved_post.author == user


@pytest.mark.django_db
def test_fetch_comments_smart_parsing(requests_mock):
    """
    Checking if comments being fetched only for existent posts.
    """
    user = SocialUser.objects.create(external_id=1, username="u", email="e")
    post = Post.objects.create(external_id=55, title="Test Post", author=user)

    url = f"https://dummyjson.com/posts/{post.external_id}/comments"
    requests_mock.get(
        url,
        json={
            "comments": [
                {"id": 1, "body": "Nice!", "user": {"username": "commentator"}}
            ]
        },
        status_code=200,
    )

    fetch_comments()

    assert Comment.objects.count() == 1
    comment = Comment.objects.first()
    assert comment.post == post
    assert comment.author_email == "commentator@example.com"
