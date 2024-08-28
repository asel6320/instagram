from django.contrib import admin

from webapp.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['image', 'content', 'author', 'like_count']
    list_display_links = ['author']
    list_filter = ['author']
    search_fields = ['author', 'content']
    fields = ['image', 'content', 'author', 'get_like_users']
    readonly_fields = ['created_at']

    def get_like_users(self, instance):
        return ", ".join([user.username for user in instance.like_users.all()])

    get_like_users.short_description = 'Liked by'

    def like_count(self, instance):
        return instance.like_users.count()

admin.site.register(Post, PostAdmin)

