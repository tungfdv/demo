from django.urls import path
from user.views import *  # noqa: F403
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('<int:user_id>/', UserGetView.as_view(), name='user_get'),
    path('<int:user_id>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:user_id>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('<int:user_id>/reset-password/', UserResetPasswordView.as_view(), name='user_reset_password'),
]
