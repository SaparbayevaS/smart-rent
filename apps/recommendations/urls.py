from django.urls import path
from .views import RecommendationView

urlpatterns = [
    path(
        "properties/<int:property_id>/recommendations/",
        RecommendationView.as_view(),
    ),
]