from django.urls import path
from .views import UserRegister, UserLogin, UserActivateAccount, UserLogout, UserPasswordForget, UserActivateResetpassword, UserResetPassword

urlpatterns = [
    path('register/', UserRegister.as_view(), name='user-register'),
    path('activate/<uidb64>/<token>/', UserActivateAccount.as_view(), name='user-activate-account'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
    path('forget-password/', UserPasswordForget.as_view(), name='user-password-forget'),
    path('user-resetpassword-validate/<uidb64>/<token>/', UserActivateResetpassword.as_view(), name='user-resetpassword-validate'),
    path('user-resetpassword/', UserResetPassword.as_view(), name='user-resetpassword'),
]