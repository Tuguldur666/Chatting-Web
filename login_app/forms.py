from django.contrib.auth import authenticate
from django import forms
from basic_app.models import UserProfile

class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
        return super(UserLoginForm, self).clean()

    class Meta:
        model = UserProfile
        fields = ['username', 'password']
