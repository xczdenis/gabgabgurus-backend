from django.db.models import Q

from gabgabgurus.common.admin.filters import InputFilter


class MessageFilterBySender(InputFilter):
    parameter_name = "sender_filter"
    title = "Sender ID or email"

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            q_filter = Q(sender__email__icontains=value)
            if value.isdigit():
                q_filter = q_filter | Q(sender__pk=int(value))
            return queryset.filter(q_filter)
        return queryset


class MessageFilterByChannel(InputFilter):
    parameter_name = "channel_filter"
    title = "Channel"

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            q_filter = Q(channel__owner__email__icontains=value)
            if value.isdigit():
                q_filter = q_filter | Q(channel__pk=int(value))
            return queryset.filter(q_filter)
        return queryset


class MessageStatusFilterByUser(InputFilter):
    parameter_name = "user_filter"
    title = "User"

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            q_filter = Q(user__email__icontains=value)
            if value.isdigit():
                q_filter = q_filter | Q(user__pk=int(value))
            return queryset.filter(q_filter)
        return queryset


class MessageStatusFilterBySender(MessageFilterBySender):
    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            q_filter = Q(message__sender__email__icontains=value)
            if value.isdigit():
                q_filter = q_filter | Q(message__sender__pk=int(value))
            return queryset.filter(q_filter)
        return queryset


class MessageStatusFilterByChannel(MessageFilterByChannel):
    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            q_filter = Q(message__channel__owner__email__icontains=value)
            if value.isdigit():
                q_filter = q_filter | Q(message__channel__pk=int(value))
            return queryset.filter(q_filter)
        return queryset


class UserChannelFilterByChannel(MessageFilterByChannel):
    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            q_filter = Q(channel__owner__email__icontains=value)
            if value.isdigit():
                q_filter = q_filter | Q(channel__pk=int(value))
            return queryset.filter(q_filter)
        return queryset
