import uuid
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Participant, Winner
from .serializer import ParticipantSerializer, PasswordSerializer
import random
from .tasks import send_winner_email


from django.http import HttpResponse
from .tasks import enviar_correo_bienvenida


def test_view(request):
    enviar_correo_bienvenida.delay("silvabravofabian@gmail.com")
    return HttpResponse("Tarea encolada")


class RegisterParticipantView(generics.CreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

# View para verificar el token y activar la cuenta
class VerifyEmailView(APIView):
    def get(self, request, token):
        participant = get_object_or_404(Participant, verification_token=token)
        return Response({'message': 'Token válido. Ingresa tu nueva contraseña.'})

    def post(self, request, token):
        participant = get_object_or_404(Participant, verification_token=token)
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participant.set_password(serializer.validated_data['password'])
        participant.is_verified = True
        participant.verification_token = None
        participant.save()

        return Response({'message': 'Tu cuenta ha sido activada. Ya estás participando en el sorteo.'})

# View para que el admin pueda ver y gestionar participantes
class ParticipantAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Participant.objects.all().order_by('-date_joined')
    serializer_class = ParticipantSerializer
    lookup_field = 'id'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        is_verified = self.request.query_params.get('is_verified')
        if is_verified in ['true', 'True', '1']:
            qs = qs.filter(is_verified=True)
        return qs

    @action(detail=False, methods=['post'])
    def draw_winner(self, request):
        verified = Participant.objects.filter(is_verified=True)
        if not verified.exists():
            return Response({'error': 'No hay participantes verificados'}, status=status.HTTP_400_BAD_REQUEST)
        winner = random.choice(list(verified))

        # Enviar correo y guardar ganador
        Winner.objects.create(participant=winner)
        send_winner_email.delay(
            winner.email, winner.first_name, winner.last_name)

        return Response({
            'winner': {
                'id': winner.id,
                'first_name': winner.first_name,
                'last_name': winner.last_name,
                'email': winner.email
            }
        })

# View para que el admin pueda ver el último ganador
class LastWinnerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        last_winner = Winner.objects.select_related(
            'participant').order_by('-date_won').first()
        if not last_winner:
            return Response({'winner': None})

        p = last_winner.participant
        return Response({
            'winner': {
                'id': p.id,
                'first_name': p.first_name,
                'last_name': p.last_name,
                'email': p.email,
                'date_won': last_winner.date_won
            }
        })

# Admin login, logout, y session check views
class AdminLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)


class AdminLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        request.user.auth_token.delete()  # elimina el token
        return Response({"message": "Logout exitoso"})


class AdminSessionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return Response({"is_authenticated": True, "username": request.user.username})
        return Response({"is_authenticated": False})
