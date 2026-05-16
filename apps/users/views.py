from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter
from apps.users.tasks import send_welcome_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

User = get_user_model()

class ProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        send_welcome_email.delay(user.email)

        return Response({"message": "User created"}, status=201)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=HTTP_200_OK)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'role']


