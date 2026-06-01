from django.db.models import Count, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from .models import Favourite, Property
from .permissions import IsOwnerOrReadOnly
from .serializers import FavouriteSerializer, PropertySerializer


class PropertyViewSet(ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "city",
        "category",
        "price",
    ]

    search_fields = ["price"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet[Property]:
        return (
            Property.objects.select_related(
                "city",
                "category",
                "owner",
            )
            .prefetch_related("images")
            .annotate(
                image_count=Count("images"),
            )
        )

    def perform_create(
        self,
        serializer: BaseSerializer,
    ) -> None:
        serializer.save(owner=self.request.user)


class FavourtiteViewSet(ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Favourite]:
        return Favourite.objects.filter(
            user=self.request.user,
        )

    def perform_create(
        self,
        serializer: BaseSerializer,
    ) -> None:
        if Favourite.objects.filter(
            user=self.request.user,
            property=serializer.validated_data["property"],
        ).exists():
            raise ValidationError(
                "Already in favourites",
            )

        serializer.save(user=self.request.user)

    def destroy(
        self,
        request: Request,
        *args,
        **kwargs,
    ):
        return super().destroy(
            request,
            *args,
            **kwargs,
        )