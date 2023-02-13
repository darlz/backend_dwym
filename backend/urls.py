from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include
from django.contrib import admin
from api_backend import views

router = routers.DefaultRouter()
router.register(r'usuarios', views.UserView)
router.register(r'cursos', views.CursoView)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),

    path('', include(router.urls)),
    
    path('registro/', views.RegistroView.as_view(), name='registro')
]
