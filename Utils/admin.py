import typing

from django.contrib import admin

if typing.TYPE_CHECKING:
    _BaseModel = admin.ModelAdmin
else:
    _BaseModel = object


class CreateOnlyMixin(_BaseModel):
    createonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        f_ = list(super().get_readonly_fields(request, obj))
        if obj:
            f_ += self.createonly_fields
        return f_
