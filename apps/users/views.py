from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView
from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter
from apps.users.tasks import send_welcome_email

User = get_user_model()

class ProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        send_welcome_email.delay(user.email)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'role']


