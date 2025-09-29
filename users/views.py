from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Participant
from .serializer import ParticipantSerializer
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


class VerifyEmailView(APIView):
    def get(self, request, token):
        participant = get_object_or_404(Participant, verification_token=token)
        participant.is_verified = True
        participant.verification_token = None
        participant.save()
        return Response({'message': 'Tu cuenta ha sido activada. Ya estás participando en el sorteo.'})

# Admin viewset for listing participants and drawing winner
class ParticipantAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Participant.objects.all().order_by('-date_joined')
    serializer_class = ParticipantSerializer
    lookup_field = 'id'

    # GET /api/admin/participants/?is_verified=true
    def get_queryset(self):
        qs = super().get_queryset()
        is_verified = self.request.query_params.get('is_verified')
        if is_verified in ['true', 'True', '1']:
            qs = qs.filter(is_verified=True)
        return qs

    @action(detail=False, methods=['post'])
    def draw_winner(self, request):
        # pick random verified participant
        verified = Participant.objects.filter(is_verified=True)
        if not verified.exists():
            return Response({'error': 'No hay participantes verificados'}, status=status.HTTP_400_BAD_REQUEST)
        winner = random.choice(list(verified))
        # Optional: Save winner record (could use a Winner model)
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
