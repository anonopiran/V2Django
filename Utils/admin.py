from django.contrib import admin


class CreateOnlyMixin:
    createonly_fields = []

    def get_readonly_fields(self: admin.ModelAdmin, request, obj=None):
        f_ = list(
            super(CreateOnlyMixin, self).get_readonly_fields(request, obj)
        )
        if obj:
            f_ += self.createonly_fields
        return f_
