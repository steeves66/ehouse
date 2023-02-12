from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'input is-info',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'input is-info',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'

        self.fields['first_name'].error_messages = {'required': 'Entrer un nom'}
        self.fields['last_name'].error_messages = {'required': 'Entrer un prénom'}
        self.fields['username'].error_messages = {'required': 'Entrer un petit nom'}
        self.fields['email'].error_messages = {'required': 'Entrer un email'}
        self.fields['phone_number'].error_messages = {'required': 'Entrer un numero pour vous contacter'}
        self.fields['password'].error_messages = {'required': 'Entrer un mot de passe'}
        self.fields['confirm_password'].error_messages = {'required': 'Confirmer mot de passe'}

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'input is-dark'

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match."
            )




class UserForgetPasswordForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Entrer un email',
        'class': 'input is-dark',
         }),
        error_messages={
            'required': "Password can't be null",
            'invalid': 'Please enter a valid email address.'
        })


    def clean(self):
        email = self.cleaned_data.get('email')
        if email is not None:
            if not User.objects.filter(email= email).exists():
                self.add_error('email', "Bad Email")            
        # if(not user):
        #     raise forms.ValidationError("Email don't exist")
        # regex = '^[a-z0-9]+[\.-_]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # if not (re.fullmatch(regex, email)):
        #     raise forms.ValidationError("Votre email n'a pas le bon format, veuillez saisir un email valide")
        # return email




class UserResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'input is-info',
    }),
    error_messages={
        'required': "Password can't be null",
        'invalid': 'Please enter a valid email address.'
    })

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'input is-info',
    }))

    def clean(self):
        cleaned_data = super(UserResetPasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match."
            )
