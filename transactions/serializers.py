from rest_framework import serializers
from .models import Transaction
from users.models import CustomUser


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'agent', 'amount', 'fee', 'status', 'transfer_code', 'created_at', 'updated_at']
        read_only_fields = ['id', 'fee', 'status', 'transfer_code', 'created_at', 'updated_at']

    def validate(self, data):
        if data['sender'] == data['receiver']:
            raise serializers.ValidationError("Sender and receiver cannot be the same user.")
        return data


class TransactionDetailSerializer(TransactionSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()
    agent = serializers.StringRelatedField()