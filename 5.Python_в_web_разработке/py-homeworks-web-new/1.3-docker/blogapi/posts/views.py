from rest_framework import generics, permissions
from .models import Post
from .permissions import IsAuthorOrReadOnly # new
from .serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
# ограничить доступ к API для аутентифицированных
# пользователей на в данном случае уровне проекта 
# (можно еще на уровне представления или объекта)
    permission_classes = (permissions.IsAuthenticated, ) # new 
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.IsAuthenticated, ) # new
    permission_classes = (IsAuthorOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer