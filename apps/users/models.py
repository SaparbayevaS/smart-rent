from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    EmailField,
    ImageField,
    IntegerField,
    Model,
    OneToOneField,
    TextField,
)


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ) -> "User":
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = EmailField(unique=True)

    objects = CustomUserManager()

    ROLE_CHOICES = (
        ("user", "User"),
        ("realtor", "Realtor"),
        ("admin", "Admin"),
    )

    role = CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []


class Profile(Model):
    user = OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="profile",
    )

    phone = CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    avatar = ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    bio = TextField(
        blank=True,
        null=True,
    )

    city = CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    budget_min = IntegerField(
        blank=True,
        null=True,
    )

    budget_max = IntegerField(
        blank=True,
        null=True,
    )

    created_at = DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return self.user.email