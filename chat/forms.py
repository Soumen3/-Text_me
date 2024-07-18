from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'required': 'required'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': 'required'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'required': 'required'}))
    email = forms.EmailField(max_length=75, required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': 'required'}))
    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'required': 'required'}))
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'required': 'required'}))
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
            attrs={
                    'class': 'form-control', 
                    'placeholder': 'Username', 
                    'required': 'required'
                }
        ))
    password = forms.CharField(widget=forms.PasswordInput(
            attrs={
                    'class': 'form-control', 
                    'placeholder': 'Password', 
                    'required': 'required'
                }
        ))
    
class ForgotUsernameForm(forms.Form):
    email = forms.EmailField(max_length=75, required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': 'required'}))


class ProfileUpadateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about', 'phone', 'country', 'birth_date')
        widgets = {
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }