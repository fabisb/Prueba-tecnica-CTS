from rest_framework import serializers
from .models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        participant = Participant(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            username=data['email'],
            phone=data.get('phone', '')
        )
        participant.set_password(data['password'])
        participant.save()

        # Enviar correo de verificación de manera asíncrona
        from .tasks import send_verification_email
        send_verification_email.delay(
            str(participant.email), str(participant.verification_token))

        return participant
