from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer
from .models import User

class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializers = SignupSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
        return Response(serializers.data, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        tokens = response.data
        request.session['access'] = tokens.get('access')
        request.session['refresh'] = tokens.get('refresh')
        request.session.save()
        return response



