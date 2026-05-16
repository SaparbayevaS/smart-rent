from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, FavourtiteViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'favourite', FavourtiteViewSet, basename='favourites')

urlpatterns = [
    path('', include(router.urls))
]