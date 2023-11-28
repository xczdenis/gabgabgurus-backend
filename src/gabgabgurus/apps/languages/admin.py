from django.contrib import admin

from gabgabgurus.apps.languages import models


class CountryLanguageInline(admin.TabularInline):
    model = models.CountryLanguage
    extra = 0
    autocomplete_fields = ("language",)


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    ordering = ("name",)


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = (CountryLanguageInline,)
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    ordering = ("name",)
