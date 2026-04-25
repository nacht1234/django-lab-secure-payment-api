from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django_ratelimit.decorators import ratelimit
import logging

from .models import Payment
from .serializers import PaymentSerializer
from .utils import encrypt_data, decrypt_data

logger = logging.getLogger('payments')

@api_view(['POST'])
def create_payment(request):
    serializer = PaymentSerializer(data=request.data)

    if serializer.is_valid():
        name = serializer.validated_data['name']
        card = serializer.validated_data['card']

        encrypted_card = encrypt_data(card)

        payment = Payment.objects.create(
            name=name,
            encrypted_card=encrypted_card
        )

        return Response({
            "message": "Payment stored securely",
            "id": payment.id
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_payment(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
        decrypted_card = decrypt_data(payment.encrypted_card)

        return Response({
            "name": payment.name,
            "card": decrypted_card
        })

    except Payment.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        return Response({"error": "Decryption failed"}, status=500)

@api_view(['POST'])
@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Missing credentials"}, status=400)

    user = authenticate(request, username=username, password=password)

    if user:
        return Response({"message": "Login successful"})
    else:
        logger.warning(f"Failed login attempt for user: {username}")
        return Response({"error": "Invalid credentials"}, status=401)