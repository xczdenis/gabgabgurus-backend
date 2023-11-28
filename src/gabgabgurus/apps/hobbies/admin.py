from django.contrib import admin

from gabgabgurus.apps.hobbies import models


@admin.register(models.Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    ordering = ("name",)
