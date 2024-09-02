from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from escrow.models import Escrow
from escrow.serializers import EscrowSerializer
from .models import Transaction
from .serializers import TransactionSerializer, TransactionDetailSerializer
from django.utils.crypto import get_random_string
import decimal


class CreateTransactionView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        amount = serializer.validated_data['amount']
        fee = self.calculate_fee(amount)
        transfer_code = self.generate_transfer_code()
        transaction = serializer.save(sender=self.request.user, fee=fee, transfer_code=transfer_code)

        Escrow.objects.create(transaction=transaction, amount=amount)

    def calculate_fee(self, amount):
        if amount <= 200:
            return decimal.Decimal('25.00')
        elif amount <= 1000:
            return decimal.Decimal('37.00')
        elif amount <= 5000:
            return decimal.Decimal('57.00')
        else:
            return amount * decimal.Decimal('0.0077')  # 0.77% for amounts over 10,000

    def generate_transfer_code(self):
        return get_random_string(20)


class ConfirmTransactionView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        transaction = self.get_object()
        if transaction.status != 'PENDING':
            return Response({"error": "Only pending transactions can be confirmed."},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.user.role != 'agent':
            return Response({"error": "Only agents can confirm transactions."},
                            status=status.HTTP_403_FORBIDDEN)

        transaction.status = 'CONFIRMED'
        transaction.agent = request.user
        transaction.save()
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)


class CompleteTransactionView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        transaction = self.get_object()
        if transaction.status != 'CONFIRMED':
            return Response({"error": "Only confirmed transactions can be completed."},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.user.role != 'agent':
            return Response({"error": "Only agents can complete transactions."},
                            status=status.HTTP_403_FORBIDDEN)

        transaction.status = 'COMPLETED'
        transaction.save()

        escrow = Escrow.objects.get(transaction=transaction)
        escrow.is_released = True
        escrow.released_at = timezone.now()
        escrow.save()

        serializer = self.get_serializer(transaction)
        return Response(serializer.data)


class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'agent':
            return Transaction.objects.all()
        return Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'agent':
            return Transaction.objects.all()
        return Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)


class EscrowDetailView(generics.RetrieveAPIView):
    queryset = Escrow.objects.all()
    serializer_class = EscrowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'agent':
            return Escrow.objects.all()
        return Escrow.objects.filter(transaction__sender=user) | Escrow.objects.filter(transaction__receiver=user)
