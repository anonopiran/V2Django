from django.contrib import admin

from Users.models import Subscription, V2RayProfile
from Utils.admin import CreateOnlyMixin


class InlineSubscriptionAdmin(admin.TabularInline):
    model = Subscription
    fields = [
        "duration",
        "volume",
        "start_date",
    ]
    readonly_fields = ["start_date", "end_date"]
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(V2RayProfile)
class V2RayProfileAdmin(CreateOnlyMixin, admin.ModelAdmin):
    createonly_fields = ["email", "uuid"]
    readonly_fields = [
        "active_system",
        "used_bandwidth",
        "v2ray_state",
        "v2ray_state_date",
        "status__bandwidth",
        "status__date",
    ]
    list_display = [
        "email",
        "active_system",
        "active_admin",
        "due_date",
        "usage",
    ]
    inlines = [InlineSubscriptionAdmin]

    @admin.display(boolean=True)
    def status__bandwidth(self, obj: V2RayProfile):
        return obj.status__bandwidth

    @admin.display(boolean=True)
    def status__date(self, obj: V2RayProfile):
        return obj.status__date

    @admin.display()
    def due_date(self, obj: V2RayProfile):
        return obj.active_subscription.end_date

    @admin.display()
    def usage(self, obj: V2RayProfile):
        abs_ = obj.used_bandwidth["total"]
        p_ = (
            obj.used_bandwidth["total_bytes"]
            / obj.active_subscription.volume
            * 100
        )
        return "{} ({:.2f} %)".format(abs_, p_)


@admin.register(Subscription)
class SubscriptionAdmin(CreateOnlyMixin, admin.ModelAdmin):
    createonly_fields = ["start_date"]
    readonly_fields = ["end_date"]
    list_display = ["user", "volume", "start_date", "end_date"]
