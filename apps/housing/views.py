from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property, Favourite
from .serializers import PropertySerializer, FavouriteSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from rest_framework.exceptions import ValidationError


class PropertyViewSet(ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated ,IsOwnerOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = ['city', 'category', 'price']

    search_fields = ['price',]
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Property.objects.select_related(
            'city',
            'category',
            'owner'
        ).prefetch_related(
            'images'
        ).annotate(
            image_count = Count('images')
        )
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FavourtiteViewSet(ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        if Favourite.objects.filter(
            user=self.request.user,
            property=serializer.validated_data['property']
        ).exists():
            raise ValidationError("Already in favourites")
        
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
