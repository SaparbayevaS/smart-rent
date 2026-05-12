from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property
from .serializers import PropertySerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg


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
