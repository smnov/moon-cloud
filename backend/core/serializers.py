import os
from django.conf import settings
from .models import File
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class FileSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    BASE_DIR = settings.BASE_DIR

    def get_name(self, obj):
        if obj.file:
            return obj.file.name
        return 'default'
    
    def change_slashes_in_path(self, path):
        '''Repair path'''
        result = path.replace('/', '\\')
        return result
    
    def human_size(self, bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
        """ Returns a human readable string representation of bytes """
        return str(bytes) + ' ' + units[0] if bytes < 1024 else self.human_size(bytes>>10, units[1:])

    def get_size(self, obj):
        path = os.path.join(self.BASE_DIR, str(obj.file), '\\')
        repaired_path = self.change_slashes_in_path(path)
        stat = os.stat(repaired_path)
        bytes = stat.st_size 
        size = self.human_size(bytes)
        return size
    
    class Meta:
        model = File
        fields = ['file', 'name','size', 'user', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data