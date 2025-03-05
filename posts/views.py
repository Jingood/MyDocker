from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment

class PostListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializers = PostSerializer(posts, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, post_id):
        return get_object_or_404(Post, id=post_id)
    
    def get(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, post_id):
        post = self.get_object(post_id)
        if post.author != request.user:
            return Response({"error": "수정 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        post = self.get_object(post_id)
        if post.author != request.user:
            return Response({"error": "삭제 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        post.delete()
        return Response({"message": "삭제되었습니다."}, status=status.HTTP_200_OK)

class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({"message": "좋아요가 취소되었습니다."}, status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            return Response({"message": "게시물을 좋아합니다."}, status=status.HTTP_200_OK)

class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, comment_id):
        return get_object_or_404(Comment, id=comment_id)
    
    def put(self, request, comment_id):
        comment = self.get_object(comment_id)
        if comment.author != request.user:
            return Response({"error": "수정 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)
        if comment.user != request.user:
            return Response({"error": "삭제 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        comment.delete()
        return Response({"message": "삭제되었습니다."}, status=status.HTTP_200_OK)

class ReplyCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, post_id, parent_id):
        post = get_object_or_404(Post, id=post_id)
        parent_comment = get_object_or_404(Comment, id=parent_id)

        if parent_comment.post != post:
            return Response({"error": "게시글이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post, parent=parent_comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentLikeAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response({"message": "좋아요가 취소되었습니다."}, status=status.HTTP_200_OK)
        else:
            comment.likes.add(request.user)
            return Response({"message": "댓글을 좋아합니다."}, status=status.HTTP_200_OK)