import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='cmontenegro',
        tipo='Cliente', 
        nombre='Carla', 
        apellido='Montenegro', 
        correo=test_user_email if test_user_email else 'cmontenegro@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='20.126.948-9',	
        direccion='1908 Calle 18 de Julio \nPuerto Montt \nChile', 
        subscrito=True, 
        imagen='perfiles/mujerjoven.jpg')

    crear_usuario(
        username='ejara',
        tipo='Cliente', 
        nombre='Emilio', 
        apellido='Jara', 
        correo=test_user_email if test_user_email else 'ejara@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='17.056.219-6', 
        direccion='120 Calle Los Leones,Estación Central, \nSantiago, RM \nChile', 
        subscrito=True, 
        imagen='perfiles/hombrejoven.jpg')

    crear_usuario(
        username='msaavedra',
        tipo='Cliente', 
        nombre='Matías', 
        apellido='Saavedra', 
        correo=test_user_email if test_user_email else 'msaavedra@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.573.102-9', 
        direccion='1344 Pasaje Las Rejas,La Reina, \nSantiago, RM \nChile', 
        subscrito=False, 
        imagen='perfiles/adulto.jpg')

    crear_usuario(
        username='afernandez',
        tipo='Cliente', 
        nombre='Alison', 
        apellido='Fernandez', 
        correo=test_user_email if test_user_email else 'afernandez@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='21.076.564-1', 
        direccion='1987 Av. Las Lomas, San Bernardo, \nSantiago, RM \nChile', 
        subscrito=False, 
        imagen='perfiles/jovenmujer.jpg')

    crear_usuario(
        username='bjana',
        tipo='Administrador', 
        nombre='Bastián', 
        apellido='Jaña', 
        correo=test_user_email if test_user_email else 'bjana@gmail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.879.585-2', 
        direccion='1806 Pasaje Parque Japonés, \nPunta Arenas \nChile', 
        subscrito=False, 
        imagen='perfiles/jovenhombre.jpg')
    
    crear_usuario(
        username='ahernandez',
        tipo='Administrador', 
        nombre='Alexis', 
        apellido='Hernández', 
        correo=test_user_email if test_user_email else 'ahernandez@gmail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='12.659.014-3', 
        direccion='129 Pasaje Margarita, Padre Hurtado, \nSantiago, RM \nChile', 
        subscrito=False, 
        imagen='perfiles/adultoh.jpg')

    crear_usuario(
        username='alejandrosuper',
        tipo='Superusuario',
        nombre='Alejandro',
        apellido='Smith.',
        correo=test_user_email if test_user_email else 'alejandrosuper@gmail.com',
        es_superusuario=True,
        es_staff=True,
        rut='12.283.985-6',
        direccion='1987 Av. Los Dominicos, Las Condes \nSantiago, RM \nChile',
        subscrito=False,
        imagen='perfiles/hombre.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Sekiro™: Shadows Die Twice - GOTY Edition',
            'descripcion': 'Sekiro™: Shadows Die Twice - GOTY Edition te sumerge en el Japón feudal, donde la honorabilidad y la venganza se entrelazan en una historia épica. Encarna a un guerrero deshonrado conocido como el "Lobo de un solo brazo", dotado con habilidades mortales y una prótesis shinobi única. Explora paisajes impresionantes y enfrenta desafíos implacables mientras te adentras en un conflicto brutal entre el deber y la redención. Domina el combate estratégico y la sigilosa infiltración para derrotar a poderosos adversarios, incluyendo a temibles jefes que pondrán a prueba tus habilidades al límite. Vive una experiencia inolvidable donde cada victoria se gana con perseverancia y precisión, en un mundo donde la muerte es solo el comienzo de tu camino hacia la gloria.',
            'precio': 60000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/Sekiro.jpeg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'KINGDOM HEARTS -HD 1.5+2.5 ReMIX-',
            'descripcion': 'KINGDOM HEARTS -HD 1.5+2.5 ReMIX- te invita a embarcarte en un viaje mágico a través de mundos encantados y personajes icónicos de Disney y Square Enix. Revive las emocionantes aventuras de Sora, un joven con el poder de la Llave Espada, mientras viaja a través de diversos universos para proteger la luz y enfrentar las fuerzas de la oscuridad. Explora mundos como el Castillo Disney, Ciudad de Halloween y la Tierra de Dragones, entre muchos otros, mientras te enfrentas a enemigos desafiantes y resuelves misterios que afectan a cada mundo. Sumérgete en una narrativa rica y compleja que combina elementos de acción, rol y amistad en una experiencia que captura la magia de los cuentos clásicos y la emoción de los videojuegos modernos.',
            'precio': 40000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/Kingdom.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Horizon Forbidden West™ Complete Edition',
            'descripcion': 'Horizon Forbidden West™ Complete Edition te transporta a un mundo vibrante y postapocalíptico, donde la naturaleza ha reclamado las ruinas de una civilización perdida. Embárcate en una aventura épica como Aloy, una valiente cazadora en busca de respuestas sobre catastróficos eventos que amenazan con destruir lo que queda de la humanidad. Explora paisajes impresionantes que van desde selvas exuberantes hasta desiertos desolados, enfrentándote a máquinas colosales y tribus hostiles en el camino. Descubre secretos ancestrales y utiliza habilidades únicas para superar desafíos estratégicos y emocionantes combates. Vive una historia inolvidable de descubrimiento y redención en un mundo donde el destino de la humanidad pende de un hilo.',
            'precio': 50000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Horizon.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Street Fighter™ 6',
            'descripcion': 'Street Fighter™ 6 continúa la legendaria saga de combate callejero con nuevos gráficos impresionantes y mecánicas de juego mejoradas. Sumérgete en intensos enfrentamientos uno contra uno con una selección de personajes clásicos y nuevos luchadores que desafiarán tus habilidades. Experimenta combates rápidos y estratégicos donde cada movimiento cuenta, desde poderosos ataques especiales hasta precisos combos. Participa en torneos globales y desafía a jugadores de todo el mundo en el modo multijugador online. Con gráficos de última generación y una jugabilidad dinámica, Street Fighter™ 6 promete llevar la experiencia de lucha callejera a nuevas alturas mientras honra la tradición y el legado de la franquicia.',
            'precio': 45000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/StreetFighte6.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Monster Hunter: World',
            'descripcion': 'Monster Hunter: World te transporta a un mundo lleno de criaturas colosales y paisajes exuberantes por explorar. Embárcate en emocionantes expediciones como un cazador experto, donde enfrentarás bestias imponentes y desafiantes en un ecosistema vivo y dinámico. Utiliza habilidades y estrategias para rastrear y derrotar monstruos épicos, recolectando recursos para mejorar tu equipo y enfrentar desafíos aún mayores. Forma equipo con otros cazadores en el modo multijugador cooperativo para realizar misiones épicas y obtener recompensas únicas. Vive una experiencia de caza incomparable donde la astucia y la valentía te llevarán a descubrir los secretos de un mundo lleno de peligros y maravillas.',
            'precio': 23000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/MonsterHunter.jpeg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'DRAGON BALL Z: KAKAROT',
            'descripcion': 'DRAGON BALL Z: KAKAROT te invita a revivir la épica saga de Dragon Ball Z desde una perspectiva totalmente nueva. Embárcate en una aventura inolvidable como Goku y otros icónicos personajes de la serie, explorando vastos mundos, combatiendo contra formidables enemigos y desbloqueando poderosas habilidades. Sumérgete en una narrativa profunda que abarca desde la llegada de los Saiyans hasta la saga de Majin Buu, experimentando momentos clave y emocionantes batallas a lo largo de la historia. Además, disfruta de actividades secundarias, como pescar, volar y entrenar, que enriquecen aún más la experiencia de juego en este universo lleno de acción y aventura.',
            'precio': 48000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/DragonBall.jpeg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'A Way Out',
            'descripcion': 'A Way Out es una experiencia única de juego cooperativo que sigue la historia de dos prisioneros, Leo y Vincent, quienes deben colaborar para escapar de la cárcel y enfrentarse a una serie de desafíos peligrosos mientras buscan venganza. El juego se destaca por su enfoque en la cooperación entre jugadores, ya que ambos deben trabajar juntos para resolver acertijos, superar obstáculos y tomar decisiones cruciales que afectan el curso de la historia. Con un enfoque cinematográfico y momentos de acción intensa, A Way Out ofrece una narrativa emocionante y una jugabilidad innovadora diseñada para ser disfrutada junto a un amigo en línea o en pantalla dividida.',
            'precio': 30000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/AWayOut.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Resident Evil 4',
            'descripcion': 'Resident Evil 4 es un clásico del survival horror que sigue a Leon S. Kennedy, un agente especial, en una misión para rescatar a la hija del presidente de los Estados Unidos, quien ha sido secuestrada por un culto misterioso en una remota zona rural de Europa. El juego presenta una mezcla única de acción y terror, con una perspectiva sobre el hombro que cambió la forma en que se experimentan los juegos de la serie Resident Evil. Enfréntate a hordas de infectados y enfrenta a enemigos desafiantes en entornos variados, desde aldeas hasta castillos antiguos. Con mecánicas de juego innovadoras y una historia envolvente llena de giros inesperados, Resident Evil 4 ha sido aclamado como uno de los mejores juegos de su género y una experiencia inolvidable para los amantes del survival horror y los juegos de acción.',
            'precio': 30000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/ResidentEvil4.jpg'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'It Takes Two',
            'descripcion': 'It Takes Two es un juego de aventuras y plataformas cooperativo desarrollado por Hazelight Studios. La historia sigue a Cody y May, una pareja que se ha convertido en muñecos debido a un hechizo, y ahora deben trabajar juntos para encontrar una manera de volver a ser humanos. Cada jugador controla a uno de los personajes y colabora en una variedad de desafíos y puzzles ingeniosos diseñados para fomentar la cooperación y la comunicación. El juego se destaca por su narrativa emotiva y humorística, así como por su jugabilidad innovadora que aprovecha al máximo la experiencia cooperativa. It Takes Two ofrece una experiencia única que celebra la amistad y la colaboración en un viaje lleno de sorpresas y momentos memorables.',
            'precio': 16000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/ItTakesTwo.jpeg'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Hogwarts Legacy',
            'descripcion': 'Hogwarts Legacy es un juego de rol de acción ambientado en el mundo mágico de Harry Potter, desarrollado por Portkey Games y publicado por Warner Bros. Interactive Entertainment. Ambientado en el siglo XIX, mucho antes de los eventos de la serie de libros de Harry Potter, el juego te permite explorar un Hogwarts expansivo y sus alrededores mientras descubres secretos antiguos y enfrentas peligrosas criaturas mágicas.',
            'precio': 30000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/Hogwarts.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Far Cry® 6',
            'descripcion': 'Far Cry® 6 es un juego de acción y aventuras desarrollado por Ubisoft. Ambientado en la ficticia isla caribeña de Yara, el juego te sitúa en medio de una revolución contra un dictador implacable conocido como Antón Castillo, interpretado por Giancarlo Esposito. Los jugadores asumen el papel de Dani Rojas, un guerrillero que lucha para liberar a su país del régimen opresivo de Castillo.',
            'precio': 48000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/FarCry.jpeg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'FINAL FANTASY VII REMAKE INTERGRADE',
            'descripcion': 'FINAL FANTASY VII REMAKE INTERGRADE es una versión mejorada para PlayStation 5 de Final Fantasy VII Remake. Incluye mejoras gráficas y un nuevo episodio protagonizado por Yuffie Kisaragi, ofreciendo una experiencia enriquecida y visualmente impresionante del clásico juego de Square Enix.',
            'precio': 70000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/FinalFantasy.jpeg'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Age Of Empires IV The Sultans Ascend',
            'descripcion': 'The Sultans Ascend (DLC) es una expansión del popular juego de estrategia en tiempo real Age of Empires IV, desarrollado por Relic Entertainment y publicado por Xbox Game Studios. Este DLC introduce nuevas campañas, civilizaciones, unidades y mecánicas de juego centradas en la historia y la influencia de los sultanes en el mundo medieval.',
            'precio': 30000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/AgeOfEmpires4TSA.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Persona 3 Reload',
            'descripcion': 'Persona 3 Reload es una versión mejorada y relanzada del aclamado juego de rol japonés Persona 3. Desarrollado por Atlus, este juego sigue la historia de un grupo de estudiantes que descubren la capacidad de invocar y controlar poderosas entidades conocidas como Personas durante la "Hora Oscura", un período de tiempo oculto entre un día y otro.',
            'precio': 70000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/Persona3.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Jurassic World Evolution 2',
            'descripcion': 'Jurassic World Evolution 2 es la secuela del popular juego de simulación de parques de dinosaurios desarrollado por Frontier Developments. En este juego, los jugadores pueden construir y gestionar su propio parque temático de dinosaurios, enfrentándose a nuevos desafíos y emocionantes mecánicas de juego basadas en la franquicia Jurassic World.',
            'precio': 27000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Jurassic.jpeg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Persona 5 Royal',
            'descripcion': 'Persona 5 Royal es una versión expandida y mejorada del aclamado juego de rol japonés Persona 5, desarrollado por Atlus. Esta versión incluye nuevos personajes, escenarios y mecánicas de juego que enriquecen aún más la experiencia original.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/Persona5.jpg'
        },
        # Categoría "RPG" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Dark Souls III',
            'descripcion': 'Dark Souls III es un juego de acción y RPG desarrollado por FromSoftware, conocido por su dificultad desafiante y su atmósfera oscura y melancólica. Ambientado en un mundo devastado por la maldición de la No Muerte, los jugadores asumen el papel de un Ashen One, explorando paisajes góticos y enfrentándose a monstruosas criaturas en busca de respuestas y una salida a la oscuridad que amenaza con consumir todo.',
            'precio': 48000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/DarkSouls.jpeg'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Baldurs Gate',
            'descripcion': 'Baldurs Gate es una serie clásica de juegos de rol desarrollada por BioWare y basada en el sistema de reglas de Dungeons & Dragons. Ambientada en el mundo de los Reinos Olvidados, los jugadores se embarcan en épicas aventuras llenas de intriga, magia y combate estratégico.',
            'precio': 30000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/BaldursGate.jpg'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Starfield',
            'descripcion': 'Starfield es un próximo juego de rol y ciencia ficción desarrollado por Bethesda Game Studios y publicado por Bethesda Softworks. Anunciado oficialmente en el E3 2018, Starfield es la primera nueva franquicia desarrollada por Bethesda en 25 años. El juego promete llevar a los jugadores a un vasto universo lleno de exploración espacial, aventuras y misterios.',
            'precio': 30000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/Starfield.jpg'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Diablo 2: Resurrected',
            'descripcion': 'Diablo 2: Resurrected es una remasterización del clásico juego de acción RPG Diablo 2, desarrollado por Blizzard Entertainment. Este juego sigue la historia del guerrero que se enfrenta a las hordas demoníacas que amenazan con destruir el mundo de Santuario.',
            'precio':20000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/DiabloII.jpeg'
        }
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['21.076.564-1', '17.056.219-6']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

