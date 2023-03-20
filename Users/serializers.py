from rest_framework import serializers

from Users.models import Subscription, V2RayProfile
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes


@extend_schema_field(OpenApiTypes.DECIMAL)
class PrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    pass


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="email", queryset=V2RayProfile.objects.all()
    )

    class Meta:
        model = Subscription
        read_only_fields = [
            "id",
            "created_at",
            "started_at",
            "state",
            "due_date",
            "downlink",
            "uplink",
            "expired_at",
        ]
        fields = read_only_fields + [
            "user",
            "duration",
            "volume",
        ]


class V2RayProfileSerializer(serializers.ModelSerializer):
    active_subscription = PrimaryKeyRelatedField(
        read_only=True, allow_null=True
    )
    active_or_latest_subscription = PrimaryKeyRelatedField(
        read_only=True, allow_null=True
    )

    class Meta:
        model = V2RayProfile
        read_only_fields = [
            "id",
            "is_active",
            "active_system",
            "active_admin",
            "admin_message",
            "active_subscription",
            "active_or_latest_subscription",
            "expired_subscription_count",
            "reserved_subscription_count",
        ]
        fields = read_only_fields + ["email", "uuid"]
