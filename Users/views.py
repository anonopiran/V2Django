from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from Users.models import Subscription, V2RayProfile
from Users.serializers import SubscriptionSerializer, V2RayProfileSerializer


class V2RayProfileViewSet(
    CreateModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = V2RayProfile.objects.all()
    serializer_class = V2RayProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = "email"
    lookup_value_regex = r"[\w@.]+"


class SubscriptionViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]
