from django.db.models.base import Model
from users.models import Posts
from rest_framework import serializers, fields

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name']


class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ['user','name','type','created_at']