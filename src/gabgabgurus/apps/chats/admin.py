from django.contrib import admin

from gabgabgurus.apps.chats import models
from gabgabgurus.apps.chats.admin_filters import (
    MessageFilterByChannel,
    MessageFilterBySender,
    MessageStatusFilterByChannel,
    MessageStatusFilterBySender,
    MessageStatusFilterByUser,
)
from gabgabgurus.common.mixins.admin import CreatedAndUpdatedAtMixin, CreatedAtMixin


@admin.register(models.Channel)
class ChannelAdmin(CreatedAtMixin, admin.ModelAdmin):
    list_display = ("id", "owner", "channel_type")
    list_display_links = ("id", "owner")
    list_select_related = ("owner",)
    autocomplete_fields = ("owner",)
    readonly_fields = ("id", "created_at")
    search_fields = ("id", "owner__email")
    fieldsets = (
        ("Base", {"fields": ("owner", "channel_type")}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at"),
                "classes": ("collapse",),
            },
        ),
    )
    list_filter = ("channel_type",)

    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super().get_search_results(request, queryset, search_term)
    #     try:
    #         search_term_as_int = int(search_term)
    #     except ValueError:
    #         pass
    #     else:
    #         queryset |= self.model.objects.filter(id=search_term_as_int)
    #     return queryset, use_distinct


@admin.register(models.UserChannel)
class UserChannelAdmin(CreatedAtMixin, admin.ModelAdmin):
    list_display = ("id", "user", "channel_id")
    list_display_links = ("id", "user")
    list_select_related = ("user", "channel", "channel__owner")
    autocomplete_fields = ("user", "channel")
    readonly_fields = ("id", "created_at")
    search_fields = ("id", "user__email")
    list_filter = (MessageFilterByChannel,)

    @staticmethod
    def channel_id(obj):
        return obj.channel.id


@admin.register(models.Message)
class MessageAdmin(CreatedAndUpdatedAtMixin, admin.ModelAdmin):
    list_display = ("id", "channel", "sender", "short_text")
    list_display_links = ("id", "channel", "sender")
    list_select_related = ("channel__owner", "sender")
    autocomplete_fields = ("channel", "sender")
    readonly_fields = ("id", "created_at", "updated_at")
    fieldsets = (
        ("Base", {"fields": ("channel", "sender", "text")}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ["collapse"],
            },
        ),
    )
    list_filter = (MessageFilterBySender, MessageFilterByChannel)
    search_fields = ("id", "sender__email", "text")

    @staticmethod
    def short_text(obj):
        return obj.text[:20] if obj.text else "N/A"


@admin.register(models.MessageStatus)
class MessageStatusAdmin(CreatedAndUpdatedAtMixin, admin.ModelAdmin):
    list_display = ("id", "user", "msg", "sender", "channel_id", "status")
    list_display_links = ("id", "user")
    list_select_related = ("user", "message", "message__sender", "message__channel")
    autocomplete_fields = ("user", "message")
    readonly_fields = ("id", "created_at", "updated_at")
    fieldsets = (
        ("Base", {"fields": ("message", "user", "status")}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ["collapse"],
            },
        ),
    )
    list_filter = (
        MessageStatusFilterBySender,
        MessageStatusFilterByChannel,
        MessageStatusFilterByUser,
        "status",
    )
    search_fields = ("id", "user__email", "message__sender__email")

    @staticmethod
    def msg(obj):
        return obj.message.text[:20]

    @staticmethod
    def sender(obj):
        return obj.message.sender.email

    @staticmethod
    def channel_id(obj):
        return obj.message.channel.id
