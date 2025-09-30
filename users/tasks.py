from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_verification_email(email, token):
    """
    Envía un correo de verificación a un participante para activar su cuenta
    y confirmar su participación en el sorteo de San Valentín.
    """
    print(f"Enviando correo de verificación a {email} con token {token}...")
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
    link = f"{frontend_url}/verify-email/{token}/"
    subject = 'Verifica tu correo y participa en el sorteo de San Valentín 💌'
    body = f"""Hola,

¡Gracias por registrarte en el sorteo de San Valentín de CTS Turismo!

Haz clic en este enlace para activar tu cuenta y participar en el sorteo:
{link}

El premio: una estadía de 2 noches todo pagado para ti y tu pareja en un hotel de ensueño ❤️

¡No pierdas la oportunidad de ganar y celebrar el amor!
"""
    send_mail(
        subject,
        body,
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'silvabravofabian@gmail.com'),
        [email],
        fail_silently=False
    )


@shared_task
def send_winner_email(email, first_name, last_name):
    """
    Envía un correo al ganador notificando que ha sido seleccionado
    en el sorteo de San Valentín y el premio que ha ganado.
    """
    subject = '🎉 ¡Felicidades! Has ganado el sorteo de San Valentín'
    body = f"""Hola {first_name} {last_name},

¡Enhorabuena! Has sido seleccionado como el ganador del sorteo de San Valentín de CTS Turismo.

Premio: una estadía romántica de 2 noches para ti y tu pareja en un hotel todo pagado 🏨💖

Nos pondremos en contacto contigo para coordinar los detalles del premio.

¡Disfruta tu premio y celebra el amor!
"""
    send_mail(
        subject,
        body,
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'silvabravofabian@gmail.com'),
        [email],
        fail_silently=False
    )


@shared_task
def enviar_correo_bienvenida(email):
    print(f"Enviando correo a {email}...")
    return f"Correo enviado a {email}"