from django.contrib import admin

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
    ]
    readonly_fields = [
        "created_at",
        "started_at",
        "due_date",
        "expired_at",
        "state",
    ]
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
    ]
    list_display = [
        "email",
        "active_system",
        "active_admin",
        "due_date",
    ]
    inlines = [InlineSubscriptionAdmin]

    @admin.display()
    def due_date(self, obj: V2RayProfile):
        if obj.active_subscription:
            return obj.active_subscription.due_date

    @admin.display(boolean=True)
    def active_system(self, obj: V2RayProfile):
        return obj.active_system


@admin.register(Subscription)
class SubscriptionAdmin(CreateOnlyMixin, admin.ModelAdmin):
    createonly_fields = ["created_at"]
    readonly_fields = [
        "started_at",
        "due_date",
        "state",
        "expired_at",
        "usage",
    ]
    list_display = [
        "user",
        "volume",
        "started_at",
        "state",
        "due_date",
        "expired_at",
    ]
