from django.urls import include, path
from rest_framework import routers
from Users.views import SubscriptionViewSet, V2RayProfileViewSet

router = routers.DefaultRouter()
router.register(r"v2rayprofile", V2RayProfileViewSet)
router.register(r"subscription", SubscriptionViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
