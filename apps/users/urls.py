from django.urls import path
from .views import ProfileDetailView, RegisterView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='users'),
]