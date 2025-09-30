from django.urls import path, include
from .views import (
    RegisterParticipantView, VerifyEmailView, ParticipantAdminViewSet,
    test_view, AdminLoginView, AdminLogoutView, AdminSessionView, LastWinnerView
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'participants', ParticipantAdminViewSet, basename='admin-participants') 

urlpatterns = [
    path('registrar/', RegisterParticipantView.as_view(), name='register-participant'), # Registro de participantes
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify-email'), # Verificación de email
    path('admin/last-winner/', LastWinnerView.as_view(), name='last-winner'), # Último ganador

    path('admin/login/', AdminLoginView.as_view(), name='admin-login'), # Login de admin
    path('admin/logout/', AdminLogoutView.as_view(), name='admin-logout'), # Logout de admin
    path('admin/session/', AdminSessionView.as_view(), name='admin-session'), # Check de sesión de admin

    path('admin/', include(router.urls)), # Rutas del admin para gestionar participantes
    path('test-task/', test_view, name='test-task'),
]
