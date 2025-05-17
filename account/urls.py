from django.urls import path
from.views import RegisterView,SendPasswordResetEmailView,UserPasswordResetView

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('send-reset-password-email/',SendPasswordResetEmailView.as_view(),name="send-reset-password-email"),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="reset-password")
]
