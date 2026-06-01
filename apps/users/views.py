from django.contrib.auth import get_user_model

from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.tasks import send_welcome_email

from .models import Profile
from .serializers import (
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
)

User = get_user_model()


class ProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Profile:
        return self.request.user.profile


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


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    filter_backends = [SearchFilter]
    search_fields = [
        "email",
        "role",
    ]