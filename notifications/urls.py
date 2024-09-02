from django.urls import path
from .views import GetNotificationsView, MarkNotificationAsReadView

urlpatterns = [
    path('', GetNotificationsView.as_view(), name='get-notifications'),
    path('mark_read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
]
