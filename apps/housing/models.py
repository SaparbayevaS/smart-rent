from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    ImageField,
    Model,
)


class City(Model):
    name = CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Category(Model):
    name = CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Property(Model):
    title = CharField(max_length=255)

    price = DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    city = ForeignKey(
        City,
        on_delete=CASCADE,
        related_name="properties",
    )

    category = ForeignKey(
        Category,
        on_delete=CASCADE,
        related_name="properties",
    )

    owner = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="properties",
    )

    created_at = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class PropertyImage(Model):
    property = ForeignKey(
        Property,
        on_delete=CASCADE,
        related_name="images",
    )

    image = ImageField(upload_to="properties/")

    def __str__(self) -> str:
        return f"Image for {self.property.title}"


class Favourite(Model):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="favourites",
    )

    property = ForeignKey(
        Property,
        on_delete=CASCADE,
        related_name="favourites",
    )

    class Meta:
        unique_together = ("user", "property")

    def __str__(self) -> str:
        return f"{self.user} - {self.property}"