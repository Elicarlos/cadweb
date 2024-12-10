from django import forms
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib.auth.forms import AuthenticationForm

class RegistroForm(forms.ModelForm):
    email =  forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirme a sua senha")
    
    class Meta:
        model = Usuario
        fields = ['nome_completo', 'telefone']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ja esta em uso')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'As senhas não coincidem')
            
            
    def save(self, commit=True):
        user = User(
            username = self.cleaned_data['email'],
            email = self.cleaned_data['email']
        )
        
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            usuario = super().save(commit=False)
            usuario.usuario = user
            usuario.save()
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}), label='Email')  