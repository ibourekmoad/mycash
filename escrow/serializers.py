from rest_framework import serializers
from .models import  Escrow


class EscrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escrow
        fields = ['id', 'transaction', 'amount', 'is_released', 'released_at']
        read_only_fields = ['id', 'released_at']