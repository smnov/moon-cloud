from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import FilesViewSet, FileViewSet, UserViewSet, UserRegister, MyTokenObtainPairView
# For media files
from django.conf import settings
from django.conf.urls.static import static

api_router = routers.DefaultRouter()

api_router.register(
    r'files',
    FilesViewSet,
    basename='files'
)

api_router.register(
    r'file/<int:pk>', 
    FileViewSet,
    basename='file'
)

api_router.register(
    r'users',
    UserViewSet,
    basename='user'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('api/register/', UserRegister.as_view()),
    path('api/login', MyTokenObtainPairView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
