from django.db import models
from transactions.models import Transaction


class Escrow(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_released = models.BooleanField(default=False)
    released_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'Escrow for Transaction {self.transaction.id}'
