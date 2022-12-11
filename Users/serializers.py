from rest_framework import serializers

from Users.models import Subscription, V2RayProfile


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="email", queryset=V2RayProfile.objects.all()
    )
    due_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Subscription
        read_only_fields = [
            "id",
            "created_at",
            "started_at",
            "state",
            "due_date",
            "usage",
            "expired_at",
        ]
        fields = read_only_fields + [
            "user",
            "duration",
            "volume",
        ]


class V2RayProfileSerializer(serializers.ModelSerializer):
    subscription_set = SubscriptionSerializer(read_only=True, many=True)
    active_subscription = SubscriptionSerializer(read_only=True)
    active_or_latest_subscription = SubscriptionSerializer(read_only=True)

    class Meta:
        model = V2RayProfile
        read_only_fields = [
            "is_active",
            "active_system",
            "active_admin",
            "admin_message",
            "active_subscription",
            "subscription_set",
            "active_or_latest_subscription",
        ]
        fields = read_only_fields + ["email", "uuid"]
