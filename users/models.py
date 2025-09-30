import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Participant(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(
    default=uuid.uuid4, unique=True, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

class Winner(models.Model):
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_won = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.first_name} {self.participant.last_name} ({self.date_won.strftime('%Y-%m-%d')})"