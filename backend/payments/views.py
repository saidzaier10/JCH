import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Invoice

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(APIView):
    def post(self, request, *args, **kwargs):
        invoice_id = request.data.get('invoice_id')
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response({'error': 'Facture introuvable'}, status=status.HTTP_404_NOT_FOUND)

        if invoice.paid:
            return Response({'error': 'Facture déjà payée'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'unit_amount': int(invoice.amount * 100),  # Amount in cents
                            'product_data': {
                                'name': f"Cotisation {invoice.registration.category.name} - {invoice.member.first_name}",
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://localhost:5173/payment/success',
                cancel_url='http://localhost:5173/payment/cancel',
                metadata={
                    'invoice_id': invoice.id,
                },
            )
            return Response({'url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        invoice_id = session.get('metadata', {}).get('invoice_id')

        if invoice_id:
            try:
                invoice = Invoice.objects.get(id=invoice_id)
                invoice.paid = True
                invoice.save()
                
                # Also mark registration as paid
                invoice.registration.paid = True
                invoice.registration.save()
                
                print(f"Payment successful for Invoice {invoice_id}")
            except Invoice.DoesNotExist:
                print(f"Invoice {invoice_id} not found")

    return HttpResponse(status=200)
