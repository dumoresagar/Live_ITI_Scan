from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from documents.models import Files
from django.utils import timezone




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 155)
    id = serializers.CharField(max_length = 15,read_only = True)
    password = serializers.CharField(max_length = 255,write_only = True)

    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

