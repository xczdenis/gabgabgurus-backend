from django.contrib import admin

from gabgabgurus.apps.user_details import models


@admin.register(models.UserLanguage)
class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "language", "language_level", "is_learning", "is_speaking")
    list_display_links = ("id", "user", "language")
    list_select_related = ("user", "language")
    list_filter = ("is_learning", "is_speaking", "language_level", "language")
    search_fields = ("id", "user__email", "user__first_name", "language__name")
    autocomplete_fields = ("user", "language")

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(models.FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "email", "processed")
    list_display_links = ("id", "first_name", "email")
    search_fields = ("id", "first_name", "email")
