from rest_framework.test import APITestCase
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model
from apps.housing.models import City, Category, Favourite, Property

User = get_user_model()

class PropertyTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test123'
        )

        self.city = City.objects.create(name='Astana')

        self.category = Category.objects.create(name='Apartment')

        self.property = Property.objects.create(
            title="Test",
            price=1000,
            city=self.city,
            category=self.category,
            owner=self.user
        )


    def test_create_property_success(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Test Property",
            "price": "1000000",
            "city": self.city.id,
            "category": self.category.id
        }

        response = self.client.post('/api/housing/properties/', data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_create_property_unauthorized(self):
        data = {
            "title": "Test Property",
            "price": "1000000",
            "city": self.city.id,
            "category": self.category.id
        }

        response = self.client.post('/api/housing/properties/', data)

        self.assertEqual(response.status_code, 403)

    def test_create_property_invalid_data(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "",
            "price": ""
        }

        response = self.client.post('/api/housing/properties/', data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

  

    
  
