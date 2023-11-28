from django.utils import formats
from django.utils.html import format_html
from rangefilter.filters import DateTimeRangeFilterBuilder


class BaseAdminFieldsMixin:
    list_display = ()
    list_filter = ()


class CreatedAtMixin(BaseAdminFieldsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display = (*self.list_display, "created_at")
        self.list_filter = (
            *self.list_filter,
            ("created_at", DateTimeRangeFilterBuilder()),
        )


class UpdatedAtMixin(BaseAdminFieldsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display = (*self.list_display, "updated_at")
        self.list_filter = (
            *self.list_filter,
            ("updated_at", DateTimeRangeFilterBuilder()),
        )


class CreatedAndUpdatedAtMixin(BaseAdminFieldsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display = (*self.list_display, "created_and_updated_at")
        self.list_filter = (
            *self.list_filter,
            ("created_at", DateTimeRangeFilterBuilder()),
            ("updated_at", DateTimeRangeFilterBuilder()),
        )

    def created_and_updated_at(self, obj):
        if hasattr(obj, "created_at") and hasattr(obj, "updated_at"):
            created_at_str = self.formatted_date(obj.created_at)
            updated_at_str = self.formatted_date(obj.updated_at)
            return format_html(f"<div>{created_at_str}</div><div>{updated_at_str}</div>")
        return ""

    @classmethod
    def formatted_date(cls, date):
        return formats.date_format(date, "DATETIME_FORMAT")
