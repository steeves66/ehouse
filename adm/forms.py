from django import forms
from user.models import User
from django.utils.translation import gettext_lazy as _

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
       	self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'

        """ self.fields['first_name'].error_messages = {'required': 'Entrer un nom'}
        self.fields['last_name'].error_messages = {'required': 'Entrer un prénom'}
        self.fields['username'].error_messages = {'required': 'Entrer un petit nom'}
        self.fields['email'].error_messages = {'required': 'Entrer un email'}
        self.fields['phone_number'].error_messages = {'required': 'Entrer un numero pour vous contacter'}
        self.fields['password'].error_messages = {'required': 'Entrer un mot de passe'}
        self.fields['confirm_password'].error_messages = {'required': 'Confirmer mot de passe'}
 """
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match."
            )



class LoginForm(forms.Form):
  username = forms.CharField(
    label=_("Your Username"), 
    widget=forms.TextInput(attrs={
        "class": "form-control", 
        "placeholder": "Username"
    }))
  password = forms.CharField(
      label=_("Your Password"),
      strip=False,
      widget=forms.PasswordInput(attrs={
        "class": "form-control", 
        "placeholder": "Password"
    }),
  )