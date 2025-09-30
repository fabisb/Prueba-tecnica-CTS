from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_verification_email(email, token):
    print(f"Enviando correo de verificación a {email} con token {token}...")
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
    link = f"{frontend_url}/verify-email/{token}/"
    subject = 'Verifica tu correo - Sorteo CTS Turismo'
    body = f'Hola,\n\nHaz clic en este enlace para activar tu cuenta y participar en el sorteo:\n{link}\n\n¡Suerte!'
    send_mail(subject, body, getattr(settings, 'DEFAULT_FROM_EMAIL', 'silvabravofabian@gmail.com'), [email], fail_silently=False)

@shared_task
def send_winner_email(email, first_name, last_name):
    subject = '¡Felicidades! Has ganado el sorteo'
    body = f'Hola {first_name} {last_name},\n\nHas sido seleccionado como ganador del premio. Nos contactaremos contigo.\n\n¡Felicitaciones!'
    send_mail(subject, body, getattr(settings, 'DEFAULT_FROM_EMAIL', 'silvabravofabian@gmail.com'), [email], fail_silently=False)

@shared_task
def enviar_correo_bienvenida(email):
    print(f"Enviando correo a {email}...")
    return f"Correo enviado a {email}"