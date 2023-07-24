from .models import File
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import FileSerializer, UserSerializer, UserSerializerWithToken, MyTokenObtainPairSerializer



class FilesViewSet(viewsets.ModelViewSet):

    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_created)

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.get()
    serializer_class = FileSerializer(many=False)
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=False)
        return Response(serializer.data)
    
    def get_queryset(self):
        return File.objects.filter(user=self.request.user, id=self.kwargs['pk'])

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegister(APIView):
    def post(self, request):
        data = request.data
        try:
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                password=make_password(data['password'])
                )
            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'User with this name already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer