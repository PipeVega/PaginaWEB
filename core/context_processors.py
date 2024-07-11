from .models import Carrito
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.safestring import SafeString
from .forms import ProductoForm, BodegaForm, IngresarForm, UsuarioForm, PerfilForm

def obtener_datos_usuario(request):
    first_name = ''
    last_name = ''
    if request.user.is_authenticated:
        usuario = User.objects.get(pk=request.user.pk)
        first_name = usuario.first_name
        last_name = usuario.last_name
    return first_name, last_name

def obtener_datos_carrito(request):
    cantidad_productos = 0
    mostrar_carrito = False
    if request.user.is_authenticated:
        usuario = User.objects.get(pk=request.user.pk)
        if request.user.perfil.tipo_usuario == 'Cliente':
            cantidad_productos = Carrito.objects.filter(cliente=request.user.perfil).count()
            mostrar_carrito = cantidad_productos > 0
    return mostrar_carrito, cantidad_productos

def get_and_clean_session_variable(request, name):
    value = ''
    if name in request.session:
        value = request.session.get(name)
        request.session[name] = ''
    return value

def obtener_mensajes(request):
    html_messages = ''
    tipo_mensajes = []
    lista_mensajes = list(messages.get_messages(request))
    html_form_errors = get_and_clean_session_variable(request, 'backend_html_form_errors')
    titulo = html_form_errors != '' or len(lista_mensajes) > 1

    if lista_mensajes:
        
        html_messages += '<div style="text-align: left">' if titulo else '<div style="text-align: center">'
        html_messages += '<strong> Mensajes informativos: </strong><ul>' if titulo else ''

        if len(lista_mensajes) == 1:
            html_messages += f'<li>{lista_mensajes[0].message}</li>' if titulo else lista_mensajes[0].message
            tipo_mensajes.append(lista_mensajes[0].level_tag)
        else:
            for mensaje in lista_mensajes:
                html_messages += f'<li>{mensaje.message}</li>'
                tipo_mensajes.append(mensaje.level_tag)

        html_messages += '</ul></div>' if titulo else '</div>'

    mensajes = SafeString(html_messages + html_form_errors)

    tipo_mensaje = ''
    if html_form_errors != '' or 'error' in tipo_mensajes:
        tipo_mensaje = 'error'
    elif 'success' in tipo_mensajes:
        tipo_mensaje = 'success'
    elif 'info' in tipo_mensajes:
        tipo_mensaje = 'info'
    
    return mensajes, tipo_mensaje

def global_render(request):
    
    first_name, last_name = obtener_datos_usuario(request)
    mostrar_carrito, cantidad_productos = obtener_datos_carrito(request)
    mensajes, tipo_mensaje = obtener_mensajes(request)

    return {
        'mostrar_carrito': mostrar_carrito,
        'cantidad_productos': cantidad_productos,
        'first_name': first_name,
        'last_name': last_name,
        'backend_messages': mensajes,
        'backend_message_type': tipo_mensaje,
    }