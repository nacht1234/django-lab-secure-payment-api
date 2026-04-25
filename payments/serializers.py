from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    card = serializers.CharField(write_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'name', 'card', 'created_at']