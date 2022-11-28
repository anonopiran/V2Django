from rest_framework import serializers

from Users.models import Subscription, V2RayProfile


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="email", queryset=V2RayProfile.objects.all()
    )

    class Meta:
        model = Subscription
        read_only_fields = [
            "created_at",
            "end_date",
        ]

        fields = read_only_fields + [
            "user",
            "duration",
            "volume",
        ]


class V2RayProfileSerializer(serializers.ModelSerializer):
    subscription_set = SubscriptionSerializer(read_only=True, many=True)
    active_subscription = serializers.SerializerMethodField()
    used_bandwidth = serializers.JSONField(read_only=True)

    class Meta:
        model = V2RayProfile
        read_only_fields = [
            "active_system",
            "active_admin",
            "admin_message",
            "active_subscription",
            "used_bandwidth",
            "status__bandwidth",
            "status__date",
            "subscription_set",
        ]
        fields = read_only_fields + ["email", "uuid"]

    @staticmethod
    def get_active_subscription(obj):
        as_ = obj.active_subscription
        if hasattr(as_, "id"):
            return SubscriptionSerializer().to_representation(as_)
        else:
            return None
