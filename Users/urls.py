from django.urls import include, path
from rest_framework import routers
from Users.models import V2RayProfile
from Users.views import SubscriptionViewSet, V2RayProfileViewSet
from django.conf import settings

router = routers.DefaultRouter()
router.register(r"v2rayprofile", V2RayProfileViewSet)
router.register(r"subscription", SubscriptionViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
