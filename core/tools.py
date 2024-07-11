from django.core.exceptions import ValidationError
from django.utils.safestring import SafeString
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import Perfil
from .forms import UsuarioForm, PerfilForm, UsuarioForm

def eliminar_registro(modelo, clave_primaria):
    eliminado, mensaje = verificar_eliminar_registro(modelo, clave_primaria, True)
    return eliminado, mensaje

def verificar_eliminar_registro(modelo, clave_primaria, debe_eliminar_registro=False):
    
    es_eliminar_usuario = True if 'User' in str(modelo) else False
    
    # Obtiene texto de la acción eliminar del modelo
    user_id = 0
    if es_eliminar_usuario:
        
        # Respaldar el usuario, en caso de tener que eliminarlo mas adelante
        registro_usuario = User.objects.get(id=clave_primaria)

        # Cambiar de modelo, pues dado que se eliminará un usuario, se debe revisar donde se usa el Perfil su perfil
        modelo = Perfil
        clave_primaria = registro_usuario.perfil.id
        
    accion_eliminar = modelo.acciones()['accion_eliminar']

    # Verificar si el registro que se quiere eliminar realmente existe en la base de datos
    if not modelo.objects.filter(pk=clave_primaria).exists():
        return False, f'¡No se puede {accion_eliminar} {clave_primaria}, ya que no existe en la Base de Datos! Revise si el registro de la tabla de {modelo._meta.verbose_name} ya fue eliminado por otro usuario.'
    
    # Obtener datos del registro que se quiere eliminar
    registro = modelo.objects.get(pk=clave_primaria)
    info_registro = str(registro)

    # Obtiene las tablas relacionadas con el modelo del registro que quiero eliminar
    tablas_relacionadas = modelo._meta.related_objects

    # Se revisarán todas las tablas que usan como clave foránea el registro que quiero eliminar
    for tabla_relacionada in tablas_relacionadas:

        # Obtiene el nombre lógico de la tabla relacionada y su campo relacionado
        modelo_relacionado = tabla_relacionada.related_model
        nombre_campo_relacionado = tabla_relacionada.field.name

        # Obtiene los nombres lógicos de las tablas relacionadas
        nombre_tabla_relacionada = modelo_relacionado._meta.verbose_name
        nombre_tabla_relacionada_plural = modelo_relacionado._meta.verbose_name_plural

        # Verifica si el registro está presente en la tabla relacionada
        if modelo_relacionado.objects.filter(**{nombre_campo_relacionado: clave_primaria}).exists():
            return False, f'¡No se puede {accion_eliminar} "{info_registro}", ya que está presente en {nombre_tabla_relacionada_plural}!'

    # Intentar eliminar el registro
    try:
        if debe_eliminar_registro:
            if es_eliminar_usuario:
                registro_usuario.delete()
                return True, f'¡El Usuario "{registro_usuario.first_name} {registro_usuario.last_name}" fue eliminado correctamente!'
            else:
                registro.delete()
                return True, f'¡El registro de {modelo._meta.verbose_name} "{info_registro}" fue eliminado correctamente!'
    except Exception as error:
        return False, f'Comuníquese con el Administrador del sistema. ¡No se pudo eliminar el {modelo._meta.verbose_name} "{info_registro}", pues se presentó el siguiente problema: {error}!'

def validar_password(password, request=None, add_error_messages=False):
    try:
        validate_password(password)
        return True
    except ValidationError as error:
        if add_error_messages:
            error_messages = '<ul>'
            for error in error.messages:
                error_messages += f'<li>{error}</li>'
            error_messages += '</ul>'
            field_name = User._meta.get_field('password').verbose_name
            messages.add_message(request, messages.ERROR, SafeString(f'{field_name}: {error_messages}'))
        return False
    
def validar_username(username, request=None, add_error_messages=False):
    validator = UnicodeUsernameValidator()
    try:
        validator(username)
        return True
    except ValidationError as e:
        if add_error_messages:
            username_verbose_name = User._meta.get_field('username').verbose_name
            messages.add_message(request, messages.ERROR, SafeString(f'{username_verbose_name}: {e.messages[0]}'))
        return False

def validar_username_repetido(username, excluded_username=None, request=None, add_error_messages=False):
    try:
        if excluded_username:
            User.objects.exclude(username=excluded_username).get(username=username)
        else:
            User.objects.get(username=username)
        if add_error_messages:
            messages.add_message(request, messages.ERROR, f'Nombre de usuario: El nombre de usuario "{username}" ya existe en la base de datos.')
        return False
    except User.DoesNotExist:
        return True
    
def show_form_errors(request, forms):

    request.session['backend_html_form_errors'] = ''

    html_form_error = ''
    for form in forms:
        for field in form:
            if field.errors:
                html_form_error += f'<strong> {field.label}: </strong><ul>'
                for error in field.errors:
                    html_form_error += f'<li>{error}</li>'
                html_form_error += '</ul>'
    if html_form_error != '':
        html_form_error = f'<div style="text-align: left">{html_form_error}</div>'
        request.session['backend_html_form_errors'] = SafeString(html_form_error)
