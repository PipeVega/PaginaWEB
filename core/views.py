from datetime import date
from .zpoblar import poblar_bd
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.utils.safestring import SafeString
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Producto, Boleta, Carrito, DetalleBoleta, Bodega, Perfil
from .forms import ProductoForm, BodegaForm, IngresarForm, UsuarioForm, PerfilForm
from .forms import RegistroUsuarioForm, RegistroPerfilForm
from .templatetags.custom_filters import formatear_dinero, formatear_numero
from .tools import eliminar_registro, verificar_eliminar_registro, show_form_errors
from django.core.mail import send_mail

def es_personal_autenticado_y_activo(user):
    return (user.is_staff or user.is_superuser) and user.is_authenticated and user.is_active

def es_usuario_anonimo(user):
    return user.is_anonymous

def es_cliente_autenticado_y_activo(user):
    return (not user.is_staff and not user.is_superuser) and user.is_authenticated and user.is_active

def index(request):

    if request.method == 'POST':
        buscar = request.POST.get('buscar')
        registros = Producto.objects.filter(nombre__icontains = buscar).order_by('nombre')

    if request.method == 'GET':
        registros = Producto.objects.all().order_by('nombre')
    
    productos = []
    for registro in registros:
        productos.append(obtener_info_producto(registro.id))
    
    context = { 'productos': productos }

    return render(request, 'core/index.html', context)

def ficha(request, producto_id):
    context = obtener_info_producto(producto_id)
    return render(request, 'core/ficha.html', context)

def nosotros(request):
    return render(request, 'core/nosotros.html')

def ropa(request):
    return render(request, 'core/ropa.html')

@user_passes_test(es_usuario_anonimo, login_url='index')
def ingresar(request):

    if request.method == 'POST':
        form = IngresarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'¡Bienvenido(a) {user.first_name} {user.last_name}!')
                    return redirect(index)
                else:
                    messages.error(request, 'La cuenta está desactivada.')
            else:
                messages.error(request, 'La cuenta o la password no son correctos')
        else:
            messages.error(request, 'No se pudo ingresar al sistema')
            show_form_errors(request, [form])

    if request.method == "GET":

        form = IngresarForm()

    context = {
        'form':  IngresarForm(),
        'perfiles': Perfil.objects.all().order_by('tipo_usuario', 'subscrito'),
    }

    return render(request, "core/ingresar.html", context)

@login_required
def salir(request):
    nombre = request.user.first_name
    apellido = request.user.last_name
    messages.success(request, f'¡Hasta pronto {nombre} {apellido}!')
    logout(request)
    return redirect(index)

@user_passes_test(es_usuario_anonimo)
def registrarme(request):
    
    if request.method == 'POST':
        
        form_usuario = RegistroUsuarioForm(request.POST)
        form_perfil = RegistroPerfilForm(request.POST, request.FILES)
        
        if form_usuario.is_valid() and form_perfil.is_valid():
            usuario = form_usuario.save()
            usuario.is_staff = False
            perfil = form_perfil.save(commit=False)
            usuario.save()
            perfil.usuario_id = usuario.id
            perfil.tipo_usuario = 'Cliente'
            perfil.save()
            mensaje = f'Tu cuenta de usuario: "{usuario.username}" ha sido creada con éxito. ¡Ya puedes ingresar a la tienda'
            messages.success(request, mensaje)
            return redirect(ingresar)
        else:
            messages.error(request, f'No fue posible crear tu cuenta de cliente.')
            show_form_errors(request, [form_usuario, form_perfil])
    
    if request.method == 'GET':
        form_usuario = RegistroUsuarioForm()
        form_perfil = RegistroPerfilForm()

    context = {
        'form_usuario': form_usuario,
        'form_perfil': form_perfil,
    }

    return render(request, 'core/registrarme.html', context)

@login_required
def misdatos(request):

    if request.method == 'POST':
        form_usuario = UsuarioForm(request.POST, instance=request.user)
        form_perfil = RegistroPerfilForm(request.POST, request.FILES, instance=request.user.perfil)
        
        if form_usuario.is_valid() and form_perfil.is_valid():
            usuario = form_usuario.save(commit=False)
            perfil = form_perfil.save(commit=False)
            usuario.save()
            perfil.usuario_id = usuario.id
            perfil.save()
            if perfil.tipo_usuario in ['Administrador', 'Superusuario']:
                tipo_cuenta = perfil.tipo_usuario
            else:
                tipo_cuenta = 'CLIENTE PREMIUM' if perfil.subscrito else 'cliente'
            messages.success(request, f'Tu cuenta de {tipo_cuenta} ha sido actualizada con éxito.')
            return redirect(misdatos)
        else:
            show_form_errors(request, [form_usuario, form_perfil])

    if request.method == 'GET':
        form_usuario = UsuarioForm(instance=request.user)
        form_perfil = RegistroPerfilForm(instance=request.user.perfil)

    context = {
        'form_usuario': form_usuario,
        'form_perfil': form_perfil
    }

    return render(request, 'core/misdatos.html', context)

@login_required
def boleta(request, nro_boleta):
    boleta = None
    detalle_boleta = None

    if Boleta.objects.filter(nro_boleta=nro_boleta).exists():
        boleta = Boleta.objects.get(nro_boleta=nro_boleta)
        boleta_es_del_usuario = Boleta.objects.filter(nro_boleta=nro_boleta, cliente=request.user.perfil).exists()
        if boleta_es_del_usuario or request.user.is_staff:
            detalle_boleta = DetalleBoleta.objects.filter(boleta=boleta)
        else:
            messages.error(request, f'Lo siento, la boleta N°{nro_boleta} pertenece a {boleta.cliente.usuario.first_name} {boleta.cliente.usuario.last_name}.')
            boleta = None
    else:
        messages.error(request, f'La boleta N°{nro_boleta} no existe en la base de datos.')

    context = {
        'boleta': boleta,
        'detalle_boleta': detalle_boleta
    }

    return render(request, 'core/boleta.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def ventas(request):
    boletas = Boleta.objects.all()
    historial =[]

    for boleta in boletas:
        boleta_historial = {
            'nro_boleta': boleta.nro_boleta,
            'nom_cliente': f'{boleta.cliente.usuario.first_name} {boleta.cliente.usuario.last_name}',
            'fecha_venta': boleta.fecha_venta,
            'fecha_despacho': boleta.fecha_despacho,
            'fecha_entrega': boleta.fecha_entrega,
            'subscrito': 'Sí' if boleta.cliente.subscrito else 'No',
            'total_a_pagar': boleta.total_a_pagar,
            'estado': boleta.estado,
        }
        historial.append(boleta_historial)

    context = {
        'historial': historial
    }

    return render(request, 'core/ventas.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def productos(request, accion, id):

    if request.method == 'POST':

        if accion == 'crear':
            form = ProductoForm(request.POST, request.FILES)

        elif accion == 'actualizar':
            form = ProductoForm(request.POST, request.FILES, instance=Producto.objects.get(id=id))

        if form.is_valid():
            producto = form.save()
            ProductoForm(instance=producto)
            messages.success(request, f'El producto "{str(producto)}" se logró {accion} correctamente.')
            return redirect(productos, 'actualizar', producto.id)
        else:
            show_form_errors(request, [form])
            messages.error(request, f'El producto no se pudo {accion} correctamente.')

    if request.method == 'GET':

        if accion == 'crear':
            form = ProductoForm()

        elif accion == 'actualizar':
            form = ProductoForm(instance=Producto.objects.get(id=id))

        elif accion == 'eliminar':
            eliminado, mensaje = eliminar_registro(Producto, id)
            messages.success(request, mensaje)
            if eliminado:
                return redirect('productos', 'crear', 0)
            form = ProductoForm(instance=Producto.objects.get(id=id))

    context = {
        'form': form,
        'productos': Producto.objects.all()
    }

    return render(request, 'core/productos.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def usuarios(request, accion, id):

    usuario = User.objects.get(id=id) if int(id) > 0 else None
    perfil = usuario.perfil if usuario else None

    if request.method == 'POST':

        form_usuario = UsuarioForm(request.POST, instance=usuario)

        form_perfil = PerfilForm(request.POST, request.FILES, instance=perfil)

        if form_usuario.is_valid() and form_perfil.is_valid():
            usuario = form_usuario.save(commit=False)
            tipo_usuario = form_perfil.cleaned_data['tipo_usuario']
            usuario.is_staff = tipo_usuario in ['Administrador', 'Superusuario']
            perfil = form_perfil.save(commit=False)
            usuario.save()
            perfil.usuario_id = usuario.id
            perfil.save()
            messages.success(request, f'El usuario {usuario.first_name} {usuario.last_name} fue guardado exitosamente.')
            return redirect(usuarios, 'actualizar', usuario.id)
        else:
            messages.error(request, f'No fue posible guardar el nuevo usuario.')
            show_form_errors(request, [form_usuario, form_perfil])

    if request.method == 'GET':

        if accion == 'eliminar':
            eliminado, mensaje = eliminar_registro(User, id)
            messages.success(request, mensaje)
            return redirect(usuarios, 'crear', '0')
        else:
            form_usuario = UsuarioForm(instance=usuario)
            form_perfil = PerfilForm(instance=perfil)

    context = {
        'form_usuario': form_usuario,
        'form_perfil': form_perfil,
        'usuarios': User.objects.all(),
    }

    return render(request, 'core/usuarios.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def bodega(request):

    if request.method == 'POST':

        producto_id = request.POST.get('producto')
        producto = Producto.objects.get(id=producto_id)
        cantidad = int(request.POST.get('cantidad'))
        for cantidad in range(1, cantidad + 1):
            Bodega.objects.create(producto=producto)
        if cantidad == 1:
            messages.success(request, f'Se ha agregado 1 nuevo "{producto.nombre}" a la bodega.')
        else:
            messages.success(request, f'Se han agregado {cantidad} productos de "{producto.nombre}" a la bodega.')

    registros = Bodega.objects.all()
    lista = []
    for registro in registros:
        vendido = DetalleBoleta.objects.filter(bodega=registro).exists()
        item = {
            'bodega_id': registro.id,
            'nombre_categoria': registro.producto.categoria.nombre,
            'nombre_producto': registro.producto.nombre,
            'estado': 'Vendido' if vendido else 'En bodega',
            'imagen': registro.producto.imagen,
        }
        lista.append(item)

    context = {
        'form': BodegaForm(),
        'productos': lista,
    }
    
    return render(request, 'core/bodega.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def obtener_productos(request):

    categoria_id = request.GET.get('categoria_id')
    productos = Producto.objects.filter(categoria_id=categoria_id)
    data = [
        {
            'id': producto.id,
            'nombre': producto.nombre,
            'imagen': producto.imagen.url
        } for producto in productos
    ]
    return JsonResponse(data, safe=False)

@user_passes_test(es_personal_autenticado_y_activo)
def eliminar_producto_en_bodega(request, bodega_id):

    nombre_producto = Bodega.objects.get(id=bodega_id).producto.nombre
    eliminado, error = verificar_eliminar_registro(Bodega, bodega_id, True)

    if eliminado:
        messages.success(request, f'Se ha eliminado el ID {bodega_id} ({nombre_producto}) de la bodega.')
    else:
        messages.error(request, error)
    
    return redirect(bodega)

@user_passes_test(es_cliente_autenticado_y_activo)
def miscompras(request):

    boletas = Boleta.objects.filter(cliente=request.user.perfil)
    historial = []
    for boleta in boletas:
        boleta_historial = {
            'nro_boleta': boleta.nro_boleta,
            'fecha_venta': boleta.fecha_venta,
            'fecha_despacho': boleta.fecha_despacho,
            'fecha_entrega': boleta.fecha_entrega,
            'total_a_pagar': boleta.total_a_pagar,
            'estado': boleta.estado,
        }
        historial.append(boleta_historial)

    context = {
        'historial': historial
    }

    return render(request, 'core/miscompras.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def administracion(request):
    return render(request, 'core/administracion.html',)

@user_passes_test(es_personal_autenticado_y_activo)
def cambiar_estado_boleta(request, nro_boleta, estado):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    if estado == 'Anulado':
        # Anular boleta, dejando la fecha de anulación como hoy y limpiando las otras fechas
        boleta.fecha_venta = date.today()
        boleta.fecha_despacho = None
        boleta.fecha_entrega = None
    elif estado == 'Vendido':
        # Devolver la boleta al estado recien vendida al dia de hoy, y sin despacho ni entrega
        boleta.fecha_venta = date.today()
        boleta.fecha_despacho = None
        boleta.fecha_entrega = None
    elif estado == 'Despachado':
        # Cambiar boleta a estado despachado, se conserva la fecha de venta y se limpia la fecha de entrega
        boleta.fecha_despacho = date.today()
        boleta.fecha_entrega = None
    elif estado == 'Entregado':
        # Cambiar boleta a estado entregado, pero hay que ver que estado actual tiene la boleta
        if boleta.estado == 'Vendido':
            # La boleta esta emitida, pero sin despacho ni entrega, entonces despachamos y entregamos hoy
            boleta.fecha_despacho = date.today()
            boleta.fecha_entrega = date.today()
        elif boleta.estado == 'Despachado':
            # La boleta esta despachada, entonces entregamos hoy
            boleta.fecha_entrega = date.today()
        elif boleta.estado == 'Entregado':
            # La boleta esta entregada, pero si se trata de un error entonces entregamos hoy
            boleta.fecha_entrega = date.today()
    boleta.estado = estado
    boleta.save()
    return redirect(ventas)

# FUNCIONES AUXILIARES PARA OBTENER: INFORMACION DE PRODUCTOS, CALCULOS DE PRECIOS Y OFERTAS

def obtener_info_producto(producto_id):

    # Obtener el producto con el id indicado en "producto_id"
    producto = Producto.objects.get(id=producto_id)

    # Se verificará cuántos productos hay en la bodega que tengan el id indicado en "producto_id".
    # Para lograrlo se filtrarán en primer lugar los productos con el id indicado. Luego, se 
    # realizará un JOIN con la tabla de "DetalleBoleta" que es donde se indican los productos
    # que se han vendido desde la bodega, sin olvidar que los modelos funcionan con Orientación
    # a Objetos, lo que hace que las consultas sean un poco diferentes a las de SQL. 
    # DetalleBoleta está relacionada con la tabla Bodega por medio de su propiedad "bodega",
    # la cual internamente agrega en la tabla DetalleBoleta el campo "bodega_id", que permite
    # que se relacione con la tabla Bodega. Para calcular cuántos productos quedan en la Bodega
    # se debe excluir aquellos que ya fueron vendidos, lo que se logra con la condición
    # "detalleboleta__isnull=False", es decir, se seleccionarán aquellos registros de Bodega
    # cuya relación con la tabla de DetalleBoleta esté en NULL, osea los que no han sido vendidos.
    # Si un producto de la Bodega estuviera vendido, entonces tendría su relación "detalleboleta"
    # con un valor diferente de NULL, ya que el campo "bodega_id" de la tabla DetalleBoleta
    # tendría el valor del id de Bodega del producto que se vendió.
    stock = Bodega.objects.filter(producto_id=producto_id).exclude(detalleboleta__isnull=False).count()
    
    # Preparar texto para mostrar estado: en oferta, sin oferta y agotado
    con_oferta = f'<span class="text-primary"> EN OFERTA {producto.descuento_oferta}% DE DESCUENTO </span>'
    sin_oferta = '<span class="text-success"> DISPONIBLE EN BODEGA </span>'
    agotado = '<span class="text-danger"> AGOTADO </span>'

    if stock == 0:
        estado = agotado
    else:
        estado = sin_oferta if producto.descuento_oferta == 0 else con_oferta

    # Preparar texto para indicar cantidad de productos en stock
    en_stock = f'En stock: {formatear_numero(stock)} {"unidad" if stock == 1 else "unidades"}'
   
    return {
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'imagen': producto.imagen,
        'html_estado': estado,
        'html_precio': obtener_html_precios_producto(producto),
        'html_stock': en_stock,
    }

def obtener_html_precios_producto(producto):
    
    precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr = calcular_precios_producto(producto)
    
    normal = f'Precio: {formatear_dinero(precio_normal)}'
    tachar = f'Precio: <span class="text-decoration-line-through"> {formatear_dinero(precio_normal)} </span>'
    oferta = f'Oferta: <span class="text-success"> {formatear_dinero(precio_oferta)} </span>'
    subscr = f'Subscrito: <span class="text-danger"> {formatear_dinero(precio_subscr)} </span>'

    if hay_desc_oferta > 0:
        texto_precio = f'{tachar}<br>{oferta}'
    else:
        texto_precio = normal

    if hay_desc_subscr > 0:
        texto_precio += f'<br>{subscr}'

    return texto_precio

def calcular_precios_producto(producto):
    precio_normal = producto.precio
    precio_oferta = producto.precio * (100 - producto.descuento_oferta) / 100
    precio_subscr = producto.precio * (100 - (producto.descuento_oferta + producto.descuento_subscriptor)) / 100
    hay_desc_oferta = producto.descuento_oferta > 0
    hay_desc_subscr = producto.descuento_subscriptor > 0
    return precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr

# VISTAS y FUNCIONES DE COMPRAS

def comprar_ahora(request):
    messages.error(request, f'El pago aún no ha sido implementado.')
    return redirect(index)

@user_passes_test(es_cliente_autenticado_y_activo)
def carrito(request):

    detalle_carrito = Carrito.objects.filter(cliente=request.user.perfil)

    total_a_pagar = 0
    for item in detalle_carrito:
        total_a_pagar += item.precio_a_pagar
    monto_sin_iva = int(round(total_a_pagar / 1.19))
    iva = total_a_pagar - monto_sin_iva

    context = {
        'detalle_carrito': detalle_carrito,
        'monto_sin_iva': monto_sin_iva,
        'iva': iva,
        'total_a_pagar': total_a_pagar,
    }

    return render(request, 'core/carrito.html', context)

def agregar_producto_al_carrito(request, producto_id):

    if es_personal_autenticado_y_activo(request.user):
        messages.error(request, f'Para poder comprar debes tener cuenta de Cliente, pero tu cuenta es de {request.user.perfil.tipo_usuario}.')
        return redirect(index)
    elif es_usuario_anonimo(request.user):
        messages.info(request, 'Para poder comprar, primero debes registrarte como cliente.')
        return redirect(registrarme)

    perfil = request.user.perfil
    producto = Producto.objects.get(id=producto_id)

    precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr = calcular_precios_producto(producto)

    precio = producto.precio
    descuento_subscriptor = producto.descuento_subscriptor if perfil.subscrito else 0
    descuento_total=producto.descuento_subscriptor + producto.descuento_oferta if perfil.subscrito else producto.descuento_oferta
    precio_a_pagar = precio_subscr if perfil.subscrito else precio_oferta
    descuentos = precio - precio_subscr if perfil.subscrito else precio - precio_oferta

    Carrito.objects.create(
        cliente=perfil,
        producto=producto,
        precio=precio,
        descuento_subscriptor=descuento_subscriptor,
        descuento_oferta=producto.descuento_oferta,
        descuento_total=descuento_total,
        descuentos=descuentos,
        precio_a_pagar=precio_a_pagar
    )

    return redirect(ficha, producto_id)

@user_passes_test(es_cliente_autenticado_y_activo)
def eliminar_producto_en_carrito(request, carrito_id):
    Carrito.objects.get(id=carrito_id).delete()
    return redirect(carrito)

@user_passes_test(es_cliente_autenticado_y_activo)
def vaciar_carrito(request):
    productos_carrito = Carrito.objects.filter(cliente=request.user.perfil)
    if productos_carrito.exists():
        productos_carrito.delete()
        messages.info(request, 'Se ha cancelado la compra, el carrito se encuentra vacío.')
    return redirect(carrito)

# CAMBIO DE PASSWORD Y ENVIO DE PASSWORD PROVISORIA POR CORREO

@login_required
def mipassword(request):

    if request.method == 'POST':

        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito, ingresa de nuevo con tu nueva contraseña.')
            return redirect(ingresar)
        else:
            messages.error(request, 'Tu contraseña no pudo ser actualizada.')
            show_form_errors(request, [form])
    
    if request.method == 'GET':

        form = PasswordChangeForm(user=request.user)

    context = {
        'form': form
    }

    return render(request, 'core/mipassword.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def cambiar_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        existe = User.objects.filter(username=username).exists()
        if existe:
            user = User.objects.get(username=username)
            if user is not None:
                if user.is_active:
                    password = User.objects.make_random_password()
                    user.set_password(password)
                    user.save()
                    enviado = enviar_correo_cambio_password(request, user, password)
                    if enviado:
                        messages.success(request, f'Una nueva contraseña fue enviada al usuario {user.first_name} {user.last_name}')
                    else:
                        messages.error(request, f'No fue posible enviar la contraseña al usuario {user.first_name} {user.last_name}, intente nuevamente más tarde')
                else:
                    messages.error(request, 'La cuenta está desactivada.')
            else:
                messages.error(request, 'La cuenta o la password no son correctos')
        else:
            messages.error(request, 'El usuario al que quiere generar una nueva contraseña ya no existe en el sistema')
    return redirect(usuarios, 'crear', '0')

def enviar_correo_cambio_password(request, user, password):
    try:
        # Revisar "CONFIGURACIÓN PARA ENVIAR CORREOS ELECTRÓNICOS A TRAVÉS DEL SERVIDOR DE GMAIL" en settings.py 
        subject = 'Cambio de contraseña GameStore'
        url_ingresar = request.build_absolute_uri(reverse(ingresar))
        message = render(request, 'common/formato_correo.html', {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_password': password,
            'link_to_login': url_ingresar,
        })
        from_email = 'info@faithfulpet.com'  # La dirección de correo que aparecerá como remitente
        recipient_list = []
        recipient_list.append(user.email)
        # Enviar el correo
        send_mail(subject=subject, message='', from_email=from_email, recipient_list=recipient_list
            , html_message=message.content.decode('utf-8'))
        return True
    except:
        return False

def poblar(request):
    # Permite poblar la base de datos con valores de prueba en todas sus tablas.
    # Opcionalmente se le puede enviar un correo único, para que los Administradores
    # del sistema puedan probar el cambio de password de los usuarios, en la página
    # de "Adminstración de usuarios".
    poblar_bd('j.perez@duocuc.cl')
    return redirect(index)