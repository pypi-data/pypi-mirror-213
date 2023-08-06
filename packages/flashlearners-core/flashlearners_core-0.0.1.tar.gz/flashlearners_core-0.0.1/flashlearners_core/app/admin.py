from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", )}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    'subscription'
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "first_name", 'subscription', "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "first_name", 'subscription', "is_staff", "is_superuser")
    list_filter = ('subscription', "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "first_name")
    ordering = ("username", "first_name", "created_at")


User_ = get_user_model()

admin.site.register(User_, UserAdmin)
admin.site.register(Bookmark)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Subscription)
admin.site.register(Guide)
admin.site.register(NovelChapter)
admin.site.register(Video)
admin.site.register(Media)
admin.site.register(Novel)
