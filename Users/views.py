from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from Users.models import Subscription, V2RayProfile
from Users.serializers import SubscriptionSerializer, V2RayProfileSerializer


class V2RayProfileViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = V2RayProfile.objects.all()
    serializer_class = V2RayProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = "email"
    lookup_value_regex = r"[\w@.]+"


class SubscriptionViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user__uuid"]
