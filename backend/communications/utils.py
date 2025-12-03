from django.core.mail import send_mail
from django.conf import settings
from django.template import Template, Context
from .models import EmailTemplate, EmailLog
import logging

logger = logging.getLogger(__name__)

def send_templated_email(recipient_email, template_key, context):
    """
    Envoie un email basé sur un template stocké en base de données.
    Log l'envoi dans EmailLog.
    """
    try:
        template = EmailTemplate.objects.get(key=template_key)
    except EmailTemplate.DoesNotExist:
        logger.error(f"Email template '{template_key}' not found.")
        return False

    # Render subject and body
    subject_template = Template(template.subject)
    body_template = Template(template.body)
    ctx = Context(context)

    subject = subject_template.render(ctx)
    body = body_template.render(ctx)

    status = 'FAILED'
    error_message = ''

    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
            html_message=body 
        )
        status = 'SENT'
    except Exception as e:
        error_message = str(e)
        logger.error(f"Failed to send email to {recipient_email}: {e}")

    # Log the attempt
    EmailLog.objects.create(
        recipient=recipient_email,
        subject=subject,
        status=status,
        error_message=error_message
    )

    return status == 'SENT'

def send_custom_email(recipient_email, subject, body):
    """
    Envoie un email personnalisé (sans template DB).
    Log l'envoi dans EmailLog.
    """
    status = 'FAILED'
    error_message = ''

    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
            html_message=body 
        )
        status = 'SENT'
    except Exception as e:
        error_message = str(e)
        logger.error(f"Failed to send custom email to {recipient_email}: {e}")

    # Log the attempt
    EmailLog.objects.create(
        recipient=recipient_email,
        subject=subject,
        status=status,
        error_message=error_message
    )

    return status == 'SENT'
