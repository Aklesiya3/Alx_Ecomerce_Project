from django.urls import path, include
from .views import RegisterView, ProfileView, LogoutView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Custom registration and profile
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # JWT token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Djoser provides a set of endpoints for user management (password reset, activation, etc.)
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
