from django.contrib import admin
from social.models import SocialUser, Post

@admin.register(SocialUser)
class SocialUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "external_id", "email", "created_at")
    list_display_links = ("username",)
    search_fields = ("username", "email", "name")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title_short", "author_link", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("title", "body", "author__username")
    # Оптимізація адмінки (теж щоб не було N+1 при виводі списку)
    list_select_related = ("author",)

    # Кастомний метод для скорочення заголовка
    def title_short(self, obj):
        return obj.title[:50] + "..." if len(obj.title) > 50 else obj.title
    title_short.short_description = "Title"

    # Кастомний метод для клікабельного посилання на автора
    def author_link(self, obj):
        return obj.author.username
    author_link.short_description = "Author"
    author_link.admin_order_field = "author__username"