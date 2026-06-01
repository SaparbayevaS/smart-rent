from django.contrib.auth import get_user_model

from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from apps.users.tasks import send_welcome_email

from .models import Profile
from .serializers import (
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
)

User = get_user_model()

@extend_schema(
    summary="Get / update profile",
    description="Authenticated user profile",
)
class ProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Profile:
        return self.request.user.profile

@extend_schema(
    summary="Register user",
    description="Creates a new user with email, password and role",
    responses={201: {"message": "User created"}},
)
class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        send_welcome_email.delay(user.email)

        return Response(
            {"message": "User created"},
            status=HTTP_201_CREATED,
        )

@extend_schema(
    summary="Login user",
    description="Returns JWT access and refresh tokens",
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=HTTP_200_OK,
        )

@extend_schema(
    summary="List users",
    description="Search users by email or role",
)
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    filter_backends = [SearchFilter]
    search_fields = [
        "email",
        "role",
    ]