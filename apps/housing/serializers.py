from typing import Any

from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    ValidationError,
)

from .models import Category, City, Favourite, Property, PropertyImage


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PropertyImageSerializer(ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "image"]


class PropertySerializer(ModelSerializer):
    images = PropertyImageSerializer(
        many=True,
        read_only=True,
    )
    images_count = IntegerField(read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "price",
            "city",
            "category",
            "owner",
            "created_at",
            "images_count",
            "images",
        ]
        read_only_fields = [
            "owner",
            "created_at",
        ]


class FavouriteSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        user = self.context["request"].user
        property_obj = attrs["property"]

        if Favourite.objects.filter(
            user=user,
            property=property_obj,
        ).exists():
            raise ValidationError("Already in favourites")

        return attrs