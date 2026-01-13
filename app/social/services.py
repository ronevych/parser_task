import logging

import requests
from django.db import transaction

from social.models import Comment, Post, SocialUser

logger = logging.getLogger(__name__)

USER_API_URL = "https://jsonplaceholder.typicode.com/users"
POST_API_URL = "https://dummyjson.com/posts"


def fetch_users():
    """
    Getting users from JSONPlaceholder and saving them to DB.
    """
    logger.info("Starting to fetch users...")

    try:
        response = requests.get(USER_API_URL, timeout=10)
        response.raise_for_status()
        users_data = response.json()

        with transaction.atomic():
            for user_item in users_data:
                user, created = SocialUser.objects.update_or_create(
                    external_id=user_item["id"],
                    defaults={
                        "username": user_item["username"],
                        "email": user_item["email"],
                        "name": user_item["name"],
                    },
                )
                # action = "Created" if created else "Updated"
                # logger.debug(f"{action} user: {user.username}")

        logger.info(f"Successfully processed {len(users_data)} users.")

    except requests.RequestException as e:
        logger.error(f"Network error while fetching users: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def fetch_posts():
    """
    Getting posts from dummyjson. Saving only when author is in DB.
    """
    logger.info("Starting to fetch posts...")

    try:
        response = requests.get(POST_API_URL, params={"limit": 0}, timeout=10)
        response.raise_for_status()
        # API dummyjson повертає dict: {"posts": [...], "total": ...}
        posts_data = response.json().get("posts", [])

        # ОПТИМІЗАЦІЯ:
        # Замість 100 запитів до БД в циклі, робимо 1 запит.
        # Створюємо мапу: {external_id: SocialUser object}
        existing_users = {user.external_id: user for user in SocialUser.objects.all()}

        created_count = 0
        skipped_count = 0

        with transaction.atomic():
            for post_item in posts_data:
                external_user_id = post_item["userId"]

                author = existing_users.get(external_user_id)

                if not author:
                    skipped_count += 1
                    continue

                Post.objects.update_or_create(
                    external_id=post_item["id"],
                    defaults={
                        "title": post_item["title"],
                        "body": post_item["body"],
                        "author": author,
                    },
                )
                created_count += 1

        logger.info(
            f"Posts processing finished. Saved/Updated: {created_count}. "
            f"Skipped (no author): {skipped_count}"
        )

    except requests.RequestException as e:
        logger.error(f"Network error while fetching posts: {e}")


def fetch_comments():
    """
    Retrieving comments comments if only Post is in our DB.
    """
    logger.info("Starting to fetch comments...")

    # 1. Отримуємо список постів, які вже є в БД
    # Використовуємо iterator(), щоб не забивати пам'ять, якщо постів тисячі
    posts = Post.objects.all().iterator()

    total_created = 0

    for post in posts:
        try:
            url = f"https://dummyjson.com/posts/{post.external_id}/comments"
            response = requests.get(url, timeout=5)

            if response.status_code == 404:
                logger.warning(f"Comments not found for post {post.external_id}")
                continue

            response.raise_for_status()
            comments_data = response.json().get("comments", [])

            if not comments_data:
                continue

            with transaction.atomic():
                for comm_item in comments_data:
                    username = comm_item.get("user", {}).get("username", "Anonymous")

                    Comment.objects.update_or_create(
                        external_id=comm_item["id"],
                        defaults={
                            "body": comm_item["body"],
                            "author_email": f"{username}@example.com",
                            "post": post,
                        },
                    )
                    total_created += 1

        except requests.RequestException as e:
            logger.error(f"Error fetching comments for post {post.external_id}: {e}")

    logger.info(f"Comments sync finished. Total processed: {total_created}")
