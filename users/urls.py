from django.urls import path, include
from .views import RegisterParticipantView, VerifyEmailView, ParticipantAdminViewSet, test_view
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'participants', ParticipantAdminViewSet, basename='participants')

urlpatterns = [
    path('registrar/', RegisterParticipantView.as_view(), name='register-participant'),
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('admin/', include(router.urls)),
    path('test-task/', test_view, name='test-task'), 

]
