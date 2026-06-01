from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavourtiteViewSet, PropertyViewSet

router = DefaultRouter()
router.register(
    r"properties",
    PropertyViewSet,
    basename="properties",
)

router.register(
    r"favourite",
    FavourtiteViewSet,
    basename="favourites",
)

urlpatterns = [
    path("", include(router.urls)),
]