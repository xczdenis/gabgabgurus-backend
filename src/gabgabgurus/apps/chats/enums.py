from django.db import models


class ChannelTypes(models.IntegerChoices):
    PRIVATE = 100, "Private"
    GROUP = 200, "Group"
    SOLO = 300, "Solo"


class MessageStatuses(models.IntegerChoices):
    CREATED = 100, "Created"
    SENT = 200, "Sent"
    DELIVERED = 300, "Delivered"
    READ = 400, "Read"
