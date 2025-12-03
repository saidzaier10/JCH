from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from content.models import Event, Convocation
from core.models import Member
from .tasks import send_email_task, send_custom_email_task
from .models import EmailTemplate

class SendConvocationView(views.APIView):
    """
    Vue pour envoyer des convocations par email.
    """
    def post(self, request):
        event_id = request.data.get('event_id')
        member_ids = request.data.get('member_ids', [])

        if not event_id or not member_ids:
            return Response({'error': 'Event ID and Member IDs required'}, status=status.HTTP_400_BAD_REQUEST)

        event = get_object_or_404(Event, id=event_id)
        
        # Ensure template exists
        template_key = 'CONVOCATION'
        if not EmailTemplate.objects.filter(key=template_key).exists():
            EmailTemplate.objects.create(
                key=template_key,
                subject="Convocation : {{ event_title }}",
                body="<p>Bonjour {{ parent_name }},</p><p>Votre enfant {{ child_name }} est convoqué à l'événement <strong>{{ event_title }}</strong>.</p><p>Date : {{ event_date }}</p><p>Lieu : {{ event_location }}</p><p>Merci de confirmer sa présence.</p>"
            )

        success_count = 0
        failed_count = 0

        for member_id in member_ids:
            try:
                member = Member.objects.get(id=member_id)
                
                # Create or update Convocation
                convocation, created = Convocation.objects.get_or_create(
                    event=event,
                    member=member
                )

                # Send Email (if parent has email, or member has email)
                # Logic: Try parent email first, then member email (if any, though we removed unique constraint, some might have it)
                # Actually, our logic allows member.email to be empty.
                # We should check parent.email.
                
                recipient_email = None
                parent_name = "Parent"
                
                if member.parent and member.parent.email:
                    recipient_email = member.parent.email
                    parent_name = member.parent.username # Or get full name
                elif member.email:
                    recipient_email = member.email
                
                if recipient_email:
                    context = {
                        'parent_name': parent_name,
                        'child_name': f"{member.first_name} {member.last_name}",
                        'event_title': event.title,
                        'event_date': event.start_time.strftime('%d/%m/%Y %H:%M'),
                        'event_location': event.location
                    }
                    
                    # Send Email asynchronously
                    send_email_task.delay(
                        recipient_email, 
                        template_key, 
                        context, 
                        convocation_id=convocation.id
                    )
                    success_count += 1 # We assume success for the API response, actual status updated by worker
                else:
                    failed_count += 1 # No email found

            except Member.DoesNotExist:
                failed_count += 1
        
        return Response({
            'message': f"{success_count} emails queued for sending.",
            'queued_count': success_count,
            'failed_count': failed_count
        })

class BulkEmailView(views.APIView):
    """
    Vue pour envoyer des emails groupés personnalisés.
    """
    def post(self, request):
        member_ids = request.data.get('member_ids', [])
        subject = request.data.get('subject')
        body = request.data.get('body')

        if not member_ids or not subject or not body:
            return Response({'error': 'Member IDs, subject and body are required'}, status=status.HTTP_400_BAD_REQUEST)

        success_count = 0
        failed_count = 0

        # Replace newlines with <br> for HTML email if it's plain text
        if '<br>' not in body and '<p>' not in body:
            body = body.replace('\n', '<br>')

        for member_id in member_ids:
            try:
                member = Member.objects.get(id=member_id)
                
                recipient_email = None
                
                if member.parent and member.parent.email:
                    recipient_email = member.parent.email
                elif member.email:
                    recipient_email = member.email
                
                if recipient_email:
                    send_custom_email_task.delay(recipient_email, subject, body)
                    success_count += 1
                else:
                    failed_count += 1
            except Member.DoesNotExist:
                failed_count += 1
        
        return Response({
            'message': f"{success_count} emails queued.",
            'queued_count': success_count,
            'failed_count': failed_count
        })
