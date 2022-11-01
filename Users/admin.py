from django.contrib import admin

from Users.models import Subscription, V2RayProfile
from Utils.admin import CreateOnlyMixin


class InlineSubscriptionAdmin(admin.TabularInline):
    model = Subscription
    fields = [
        "duration",
        "volume",
        "start_date",
        "end_date",
        "start_volume",
        "end_volume",
    ]
    readonly_fields = ["start_date", "end_date", "start_volume", "end_volume"]
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(V2RayProfile)
class V2RayProfileAdmin(CreateOnlyMixin, admin.ModelAdmin):
    createonly_fields = ["email", "uuid"]
    readonly_fields = [
        "active_system",
        "system_message",
        "used_bandwidth",
        "v2ray_state",
        "v2ray_state_date",
    ]
    list_display = ["email", "active_system", "active_admin"]
    inlines = [InlineSubscriptionAdmin]


@admin.register(Subscription)
class SubscriptionAdmin(CreateOnlyMixin, admin.ModelAdmin):
    createonly_fields = ["start_date", "start_volume"]
    readonly_fields = ["end_date", "end_volume"]
    list_display = ["user", "end_date", "end_volume"]
