from django.db import models
from users.models import Participant


class Winner(models.Model):
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE)
    draw_date = models.DateTimeField(auto_now_add=True)
