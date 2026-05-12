from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Property, PropertyImage, City, Category

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PropertyImageSerializer(ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']

class PropertySerializer(ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    images_count = IntegerField(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'price',
            'city',
            'category',
            'owner',
            'created_at',
            'images_count',
            'images',
        ]
        read_only_fields = ['owner', 'created_at']