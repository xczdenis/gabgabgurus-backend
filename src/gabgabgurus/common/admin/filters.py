from django.contrib import admin


class InputFilter(admin.SimpleListFilter):
    template = "admin/input_filter.html"

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        query_params = changelist.get_filters_params()
        all_choice["query_parts"] = ((k, v) for k, v in query_params.items() if k != self.parameter_name)
        yield all_choice
