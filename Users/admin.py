from django.contrib import admin

from Users.models import Subscription, V2RayProfile
from Utils.admin import CreateOnlyMixin
from humanize import naturalsize
from django.utils.formats import localize


class InlineSubscriptionAdmin(admin.TabularInline):
    model = Subscription
    fields = [
        "duration",
        "volume",
        "started_at",
        "due_date",
        "expired_at",
        "state",
    ]
    readonly_fields = [
        "created_at",
        "started_at",
        "due_date",
        "expired_at",
        "state",
    ]

    @admin.display()
    def due_date(self, obj: Subscription):
        return localize(obj.due_date)

    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(V2RayProfile)
class V2RayProfileAdmin(CreateOnlyMixin, admin.ModelAdmin):
    createonly_fields = ["email", "uuid"]
    readonly_fields = [
        "calc__active_system",
        "v2ray_state",
        "v2ray_state_date",
    ]
    list_display = [
        "email",
        "calc__active_system",
        "active_admin",
        "v2ray_state",
        "due_date",
        "usage",
    ]
    inlines = [InlineSubscriptionAdmin]
    search_fields = ["email", "uuid"]
    list_filter = ("v2ray_state", "active_admin")

    @admin.display(boolean=True)
    def active_system(self, obj: V2RayProfile):
        return obj.calc__active_system

    @admin.display()
    def usage(self, obj: V2RayProfile):
        u_ = obj.active_or_latest_subscription
        if u_:
            return f"{naturalsize(u_.downlink + u_.uplink, binary=True)}/{naturalsize(u_.volume, binary=True)}"


@admin.register(Subscription)
class SubscriptionAdmin(CreateOnlyMixin, admin.ModelAdmin):
    createonly_fields = ["created_at"]
    readonly_fields = [
        "usage_downlink",
        "usage_uplink",
        "usage_total",
        "started_at",
        "due_date",
        "state",
        "expired_at",
    ]
    list_display = [
        "user",
        "volume",
        "started_at",
        "usage_total",
        "state",
        "due_date",
        "expired_at",
    ]

    @admin.display()
    def due_date(self, obj: Subscription):
        return localize(obj.due_date)

    @admin.display()
    def usage_downlink(self, obj: Subscription):
        return naturalsize(obj.downlink, binary=True)

    @admin.display()
    def usage_uplink(self, obj: Subscription):
        return naturalsize(obj.uplink, binary=True)

    @admin.display()
    def usage_total(self, obj: Subscription):
        return naturalsize(obj.downlink + obj.uplink, binary=True)
