from django.contrib import admin

from Upstream.models import Server


@admin.register(Server)
class V2RayProfileAdmin(admin.ModelAdmin):
    pass
