from .models import File
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import FileSerializer, UserSerializer



class FileViewSet(viewsets.ModelViewSet):

    serializer_class = FileSerializer

    def list(self, request):
        queryset = File.objects.get(user__pk=request.user.pk)
        serializer = FileSerializer(queryset)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.get()
    serializer_class = UserSerializer

class UserProfileView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        queryset = request.user
        serializer = UserSerializer(queryset, many=False)
        return Response(serializer.data)
