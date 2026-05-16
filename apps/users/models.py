from django.db.models import Model, EmailField, CharField, OneToOneField, CASCADE, ImageField, TextField, IntegerField, DateField, DateTimeField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

class CustimUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None

    email = EmailField(unique=True)

    objects = CustimUserManager()

    ROLE_CHOICES = (
        ('user', 'User'),
        ('realtor', 'Realtor'),
        ('admin', 'Admin'),
    )

    role = CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Profile(Model):
    user = OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='profile'
    )

    phone = CharField(max_length=20, blank=True, null=True)
    avatar = ImageField(upload_to='avatars/', blank=True, null=True)
    bio = TextField(blank=True, null=True)

    city = CharField(max_length=100, blank=True, null=True)
    budget_min = IntegerField(blank=True, null=True)
    budget_max = IntegerField(blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}"
