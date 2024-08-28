from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'gender', 'phone', 'follower_count']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'gender', 'groups']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'avatar', 'description', 'phone', 'gender')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )

    readonly_fields = ['last_login', 'date_joined']

    def follower_count(self, instance):
        return instance.followers.count()

    follower_count.short_description = 'Number of Followers'


admin.site.register(User, UserAdmin)

