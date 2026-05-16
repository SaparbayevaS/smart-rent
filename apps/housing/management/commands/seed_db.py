from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from apps.housing.models import City, Category

User = get_user_model()

class Command(BaseCommand):
    help = "Seed base data"

    def handle(self, *args, **kwargs):
        cities = ["Astana", "Almaty", "Karaganda"]
        for c in cities:
            City.objects.get_or_create(name=c)

        categories = ["Apartment", "Apt", "House", "Studio"]
        for cat in categories:
            Category.objects.get_or_create(name=cat)

        User.objects.get_or_create(
            email="admin@test.com",
            defaults={
                "role": "admin",
                "is_staff": True,
                "is_superuser": True
            }
        )

        self.stdout.write(self.style.SUCCESS("Seed DB Done"))