from django.db import models
from users.models import CustomUser


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    sender = models.ForeignKey(CustomUser, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_transactions', on_delete=models.CASCADE)
    agent = models.ForeignKey(CustomUser, related_name='handled_transactions',  null=True,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    transfer_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Transaction {self.id} - {self.status}'
