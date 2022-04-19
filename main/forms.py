from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
     
        fields =  ['nickname']
    
    
    def signup(self, request, user):
        user.nickname = self.cleaned_data["nickname"]

        user.save()

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields =  ['email','password']
        widgets = {
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control'
                }
            ),
   
        }
    
