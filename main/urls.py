from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from main import views, serializers

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)


auth_urlpatterns = [
    # i use custom django rest template for login and logout
    path('accounts/', include('rest_framework.urls')),
    # and Django REST Registration for register etc.
    path('accounts/', include('rest_registration.api.urls')),
]

urlpatterns = [
    path('', include(router.urls)),
    
    path('analitics/', views.get_likes_by_period),

    path('token/', jwt_views.TokenObtainPairView.as_view(serializer_class=serializers.MyTokenObtainPairSerializer), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(serializer_class=serializers.MyTokenObtainPairSerializer), name='token_refresh'),
]

urlpatterns += auth_urlpatterns
