from django import forms
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib.auth.forms import AuthenticationForm

class RegistroForm(forms.ModelForm):
    nome_completo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    telefone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email =  forms.EmailField(required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Confirme a sua senha")
    
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
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))  