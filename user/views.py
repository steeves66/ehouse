from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegistrationForm, UserForgetPasswordForm, UserResetPasswordForm
from .models import User
from user import signals

class UserRegister(View):
    form_class = UserRegistrationForm
    template_name = 'user/user_register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST) 
        if form.is_valid(): 
            user_instance = User(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                username = form.cleaned_data['username'],
                phone_number = form.cleaned_data['phone_number'],
                email = form.cleaned_data['email'],
                password = make_password(form.cleaned_data['password'])
                )
            user_instance.request = request
            user_instance.save()
            messages.success(request, 'Your account is created successfully. We have sent you a verification email to verify your email. Follow the instruction in this email.')   
            to_email =form.cleaned_data['email']
            return redirect('/user/login/?command=verification&email='+to_email)
        return render(request, self.template_name, {'form': form})




class UserLogin(View):
    template_name = 'user/user_login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_name = User.objects.get(username=username)
        except User.DoesNotExist:
            user_name = User.objects.get(email=username)
        user = auth.authenticate(username=user_name, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            messages.success(request, 'Login successfully')
            return redirect(reverse('home'))
        messages.error(request, 'Invalid credentials, please check username/email or password.')
        return render(request, self.template_name)




class UserActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Congratulations! Your account is activated.')
            return redirect(reverse('user-login'))




class UserLogout(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are logged out.')
        return redirect('/home/')




class UserPasswordForget(View):
    form_class = UserForgetPasswordForm
    template_name = 'user/user_password_forget.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            signals.user_password_reset_email.send(sender=self.__class__, user=user, request=request)
            messages.success(request, 'We have sent you an reset password link to your mail. Follow the instruction in this email.')
            return redirect('/user/login/?command=reset-password&email='+email)
        return render(request, self.template_name, {'form': form})




class UserActivateResetpassword(View):  
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, 'Please reset your password')
            return redirect(reverse('user-resetpassword'))
        else:
            messages.error(request, 'This link has been expired!')
            return redirect(reverse('login'))




class UserResetPassword(View):
    form_class = UserResetPasswordForm
    template_name = 'user/user_reset_password.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserResetPasswordForm(request.POST)
        if form.is_valid():
            password = make_password(form.cleaned_data.get('password'))
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.password = password
            user.save()
            messages.success(request, 'Password resetting successfully!')
            return redirect('/user/login/')
        return render(request, self.template_name, {'form': form})