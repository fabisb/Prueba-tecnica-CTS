from rest_framework import serializers
from .models import Participant
from .tasks import send_verification_email


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email','phone', 'is_verified']

    def create(self, validated_data):
        participant = Participant(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email'],
            phone=validated_data.get('phone', '')
        )
        participant.save()

        print("🚀 ~ file: users/serializer.py:20 ~ ParticipantSerializer ~ create ~ participant:", participant)
        # Enviar correo de verificación de manera asíncrona
        send_verification_email.delay(
            str(participant.email), str(participant.verification_token)
        )
        # send_verification_email.apply(args=[str(participant.email), str(participant.verification_token)])

        return participant

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=3)