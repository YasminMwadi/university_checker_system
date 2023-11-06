from typing import Any
import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model



class UploadFileForm(forms.Form):
    file = forms.FileField()


# reset password form
class CustomPasswordResetConfirmForm(forms.Form):
     password1 = forms.CharField(widget=forms.PasswordInput(
         attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker', 'placeholder': 'Password'}))
     password2 = forms.CharField(widget=forms.PasswordInput(
         attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker', 'placeholder': 'Confirm Password'}))
# send email for reset password form
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email address",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker',
            'placeholder': 'Email address',
            'required': 'required'
        }),
    )

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker', 
                'placeholder': 'Username', 'id': 'id_username'}),
        label=False,
        required=False
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker', 
                'placeholder': 'Full Name',  'id': 'id_name'}),
        label=False,
        required=False
    )
    
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker',
               'placeholder': 'Email Address',  'id': 'id_email'}),
        label=False,
        required=False,     
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker',
                  'placeholder': 'Password', 'id': 'id_password'}),
        label=False,
        required=False
    )

    verify_pwd = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker',
                   'placeholder': 'Confirm Password',  'id': 'id_confirm'}),
        label=False,
        required=False
    )

    # Checking errors: 

    # Check if the first name contains a special character
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:\'",<>\./?\\|]', first_name):
            raise ValidationError("First name cannot contain special characters.")

        return first_name
    
    #Check if email already exist in the system

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists. Please use a different email.")
        return email

    # Check password integrity
    def validate_password(self, password):
        # Minimum length of 6 characters
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        
        # At least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")                                               
       # Check if the password contains at least one special character
        if not re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:\'",<>\./?\\|]', password):
            raise ValidationError("Password must contain at least one special character.")
        
        # Check if the password contains at least one integer
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one number.")
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        self.validate_password(password)
        return password

    # Check if the passwords match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        verify_pwd = cleaned_data.get('verify_pwd')

        if password and verify_pwd and password != verify_pwd:
            raise forms.ValidationError("MAKE SURE PASSWORDS MATCH!")

        return cleaned_data


    class Meta:
        model = User
        fields = ('username','first_name', 'email', 'password')
