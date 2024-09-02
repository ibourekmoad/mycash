from django.urls import path
from .views import CreateTransactionView, ConfirmTransactionView, TransactionDetailView, TransactionListView, \
    CompleteTransactionView, EscrowDetailView

urlpatterns = [
    path('create/', CreateTransactionView.as_view(), name='create-transaction'),
    path('confirm/<int:pk>/', ConfirmTransactionView.as_view(), name='confirm-transaction'),
    path('complete/<int:pk>/', CompleteTransactionView.as_view(), name='complete-transaction'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('escrow/<int:pk>/', EscrowDetailView.as_view(), name='escrow-detail'),
]