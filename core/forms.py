from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Categoria, Producto, Perfil

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(),
            'imagen': forms.FileInput(attrs={'class': 'd-none'}),
        }
        labels = {
            'nombre': 'Nombre',
            'descuento_subscriptor': 'Subscriptor(%)',
            'descuento_oferta': 'Oferta(%)',
        }

class BodegaForm(Form):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label='Categoría')
    producto = forms.ModelChoiceField(queryset=Producto.objects.none(), label='Producto')
    cantidad = forms.IntegerField(label='Cantidad')
    class Meta:
        fields = '__all__'
       
class IngresarForm(Form):
    username = forms.CharField(widget=forms.TextInput(),label='Cuenta')
    password = forms.CharField(widget=forms.PasswordInput(),label='Contraseña')
    class Meta:
        fields = ['username', 'password']

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'email': 'E-mail'
        }

class RegistroPerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['rut', 'direccion', 'subscrito', 'imagen']
        exclude = ['tipo_usuario']
        widgets = {
            'direccion': forms.Textarea(),
            'imagen': forms.FileInput()
        }

class UsuarioForm(ModelForm):
   class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'email': 'E-mail'
        }

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['tipo_usuario', 'rut', 'direccion', 'subscrito', 'imagen']
        widgets = {
            'direccion': forms.Textarea(),
            'imagen': forms.FileInput()
        }