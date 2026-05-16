from rest_framework.serializers import ModelSerializer, CharField, EmailField, ValidationError, Serializer
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth import authenticate

User = get_user_model()

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'phone',
            'avatar',
            'bio',
            'city',
            'budget_min',
            'budget_max',
        ]
    
class RegisterSerializer(ModelSerializer):
    
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'role',
        ]

        def create(self, validated_data):
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                role=validated_data.get('role', 'user')
            )
            return user
        
class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data["email"],
            password=data["password"]
        )

        if not user:
            raise ValidationError("Invalid credentials")
        
        data["user"] = user
        return data