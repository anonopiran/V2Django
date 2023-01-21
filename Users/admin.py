from django.contrib import admin
from django.utils.formats import localize
from humanize import naturalsize

from Users.forms import SubscriptionForm
from Users.models import Subscription, V2RayProfile
from Utils.admin import CreateOnlyMixin


class InlineSubscriptionAdmin(admin.TabularInline):
    model = Subscription
    fields = [
        "duration",
        "volume",
        "started_at",
        "due_date",
        "expired_at",
        "state",
        "usage",
    ]
    readonly_fields = [
        "created_at",
        "started_at",
        "due_date",
        "expired_at",
        "state",
        "usage",
    ]

    @admin.display()
    def due_date(self, obj: Subscription):
        return localize(obj.due_date)

    @admin.display()
    def usage(self, obj: Subscription):
        return _calc__usage_total(obj)

    show_change_link = True
    form = SubscriptionForm
    extra = 0


@admin.register(V2RayProfile)
class V2RayProfileAdmin(CreateOnlyMixin, admin.ModelAdmin):
    createonly_fields = ["email", "uuid"]
    readonly_fields = [
        "active_system",
        "v2ray_state",
        "v2ray_state_date",
    ]
    list_display = [
        "email",
        "active_system",
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
        return obj.active_system

    @admin.display()
    def usage(self, obj: V2RayProfile):
        u_ = obj.active_or_latest_subscription
        if u_:
            return _calc__usage_total(u_)

    @admin.display()
    def due_date(self, obj: V2RayProfile):
        u_ = obj.active_subscription
        if u_:
            return u_.due_date


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
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
        "volume_gb",
        "started_at",
        "usage_total",
        "state",
        "due_date",
        "expired_at",
    ]

    form = SubscriptionForm
    autocomplete_fields = ["user"]
    list_filter = ["state"]

    @admin.display(description="volume")
    def volume_gb(self, obj: Subscription):
        return naturalsize(obj.volume, binary=True)

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
        return _calc__usage_total(obj)

    def save_form(self, request, form, change):
        return super().save_form(request, form, change)


def _calc__usage_total(obj: Subscription):
    return f"{naturalsize(obj.downlink + obj.uplink, binary=True)}/{naturalsize(obj.volume, binary=True)}"
