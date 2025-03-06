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
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('api/profile/change_password/', views.ChangePasswordAPIView.as_view(), name="change_pw"),
    path('api/delete/', views.DeleteUserAPIView.as_view(), name='delete'),
    path('api/profile/', views.ProfileAPIView.as_view(), name="profile"),
]
