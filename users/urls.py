from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, ProfileView, UpdateProfileView, AssignAgentView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('assign-agent/<int:user_id>/', AssignAgentView.as_view(), name='assign-agent'),

]