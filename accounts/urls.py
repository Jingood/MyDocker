from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)


urlpatterns = [
    path('api/signup/', views.SignupAPIView.as_view(), name='signup'),
    path('api/login/', views.CustomTokenObtainPairView.as_view(), name='login'),
]
