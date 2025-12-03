from celery import shared_task
from celery import shared_task
from .utils import send_templated_email, send_custom_email
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_email_task(recipient_email, template_key, context, convocation_id=None):
    """
    Celery task to send an email asynchronously.
    """
    logger.info(f"Starting email task for {recipient_email}")
    success = send_templated_email(recipient_email, template_key, context)
    
    if convocation_id and success:
        from content.models import Convocation
        from django.utils import timezone
        try:
            convocation = Convocation.objects.get(id=convocation_id)
            convocation.status = 'SENT'
            convocation.sent_at = timezone.now()
            convocation.save()
        except Convocation.DoesNotExist:
            logger.error(f"Convocation {convocation_id} not found during email task update.")
    
    return success

@shared_task
def send_custom_email_task(recipient_email, subject, body):
    """
    Celery task to send a custom email asynchronously.
    """
    logger.info(f"Starting custom email task for {recipient_email}")
    return send_custom_email(recipient_email, subject, body)
