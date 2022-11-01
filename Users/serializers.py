from rest_framework import serializers

from Users.models import Subscription, V2RayProfile


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="email", queryset=V2RayProfile.objects.all()
    )

    class Meta:
        model = Subscription
        read_only_fields = [
            "start_date",
            "start_volume",
            "end_date",
            "end_volume",
        ]

        fields = read_only_fields + [
            "user",
            "duration",
            "volume",
        ]


class V2RayProfileSerializer(serializers.ModelSerializer):
    subscription_set = SubscriptionSerializer(read_only=True, many=True)
    active_subscription = serializers.SerializerMethodField()

    class Meta:
        model = V2RayProfile
        read_only_fields = [
            "active_system",
            "active_admin",
            "system_message",
            "admin_message",
            "active_subscription",
        ]
        fields = read_only_fields + ["email", "uuid", "subscription_set"]

    @staticmethod
    def get_active_subscription(obj):
        as_ = obj.active_subscription
        if hasattr(as_, "id"):
            return SubscriptionSerializer().to_representation(as_)
        else:
            return None
