from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('criar_sala/', views.Criar_Sala, name='criar_sala'),
    path('adicionar_usuario/', views.adicionar_usuario_na_sala, name='adicionar_usuario_na_sala'),
    path('enviar-mensagem/', views.enviar_mensagem, name='enviar_mensagem'),
    path('sala/<int:sala_id>/mensagens/', views.listar_mensagens, name='listar_mensagens'),
    path('salas/', views.listar_salas, name='listar_salas'),
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]