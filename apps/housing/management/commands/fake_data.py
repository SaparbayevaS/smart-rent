import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.housing.models import City, Category, Property

User = get_user_model()

class Command(BaseCommand):
    help = "Create fake properties"

    def handle(self, *args, **kwargs):

        user = User.objects.first()
        cities = list(City.objects.all())
        categories = list(Category.objects.all())

        for i in range(20):
            Property.objects.create(
                title=f"Property {i}",
                price=random.randint(100000, 1000000),
                city=random.choice(cities),
                category=random.choice(categories),
                owner=user
            )


        self.stdout.write(self.style.SUCCESS("Fake data created"))