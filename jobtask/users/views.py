from django.shortcuts import render
from users.serializers import CreateUserSerializer, UserSerializer, PostsSerializer
from users.models import User, Posts
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
# Create your views here.


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_auth(request):
    
    serialized = CreateUserSerializer(data=request.data)

    if serialized.is_valid():
        new_user = User.objects.create_user(
            email=serialized.initial_data['email'],
            password=serialized.initial_data['password'],
        )
        
        return Response({
            'user': UserSerializer(new_user, context={'request': request}).data
        })
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAllViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsAuthenticated,)
