from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_admin_inline_paginator.admin import TabularInlinePaginated

from gabgabgurus.apps.user_details.models import UserLanguage
from gabgabgurus.apps.users import models


class UserLanguagesInline(TabularInlinePaginated):
    model = UserLanguage
    extra = 0
    autocomplete_fields = ("language",)
    pagination_key = "user-languages-page"
    per_page = 10
    ordering = ("id",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("language")
        return qs


class BlockedUsersInline(TabularInlinePaginated):
    model = models.User.blocked_users.through
    fk_name = "from_user"
    extra = 0
    verbose_name = "Blocked User"
    verbose_name_plural = "Blocked Users"
    autocomplete_fields = ["to_user"]
    pagination_key = "blocked-user-page"
    per_page = 10
    ordering = ("id",)


@admin.register(models.User)
class UserAdminView(UserAdmin):
    inlines = (UserLanguagesInline, BlockedUsersInline)
    raw_id_fields = ("country",)
    list_display = ("id", "email", "first_name", "last_name")
    list_display_links = ("id", "email")
    search_fields = ("id", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        ("Credentials", {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                    "country",
                    "about_me",
                    "hobbies",
                )
            },
        ),
        ("Staff", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
        ("Activity", {"fields": ("last_activity", "date_joined", "last_login")}),
    )
    filter_horizontal = ("hobbies", "groups")
    ordering = ("email",)
    autocomplete_fields = ("country",)
