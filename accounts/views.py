from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, PasswordChangeSerializer
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer

class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializers = SignupSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
        return Response(serializers.data, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data
        user_id = serializer.user.id

        response = Response(tokens, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=tokens.get('access'),
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        response.set_cookie(
            key='refresh_token',
            value=tokens.get('refresh'),
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        response.set_cookie(
            key='user_id',
            value=user_id,
            httponly=False,
            secure=False,
            samesite='Lax'
        )
        return response

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"error":"Refresh Not Found."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({"error": f"Token Blacklisting failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        response.delete_cookie('user_id')
        return response
    
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                pass

        user = request.user
        user.delete()

        response = Response({"detail": "User deleted Successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        response.delete_cookie('user_id')
        return response
    
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        my_posts = Post.objects.filter(author=user).order_by('-created_at')
        my_posts_serializer = PostSerializer(my_posts, many=True)

        my_comments = Comment.objects.filter(author=user).order_by('-created_at')
        my_comments_serializer = CommentSerializer(my_comments, many=True)

        liked_posts = Post.objects.filter(likes=user).order_by('-created_at')
        liked_posts_serializer = PostSerializer(liked_posts, many=True)

        return Response({
            "my_posts": my_posts_serializer.data,
            "my_comments": my_comments_serializer.data,
            "liked_posts": liked_posts_serializer.data
        }, status=status.HTTP_200_OK)