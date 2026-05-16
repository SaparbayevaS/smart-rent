from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.housing.models import Property

import logging

logger = logging.getLogger(__name__)


class RecommendationView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, property_id):

        logger.info("Recommmendations endpoind called")

        property_obj = Property.objects.get(id=property_id)

        recommendations = Property.objects.filter(
            city=property_obj.city,
            category=property_obj.category
        ).exclude(
            id=property_obj.id
        )[:5]

        data = [
            {
                "id": item.id,
                "title": item.title,
                "price": str(item.price),
            }
            for item in recommendations
        ]

        return Response(data)