$(document).ready(function() {

  // Asignar placeholders para ayudar a los usuarios
  $('#id_username').attr('placeholder', 'Ej: cgomezv, cevans, sjohasson');
  $('#id_first_name').attr('placeholder', 'Ej: Cristián, Chris, Scarlett');
  $('#id_last_name').attr('placeholder', 'Ej: Gómez Vega, Evans, Johansson');
  $('#id_email').attr('placeholder', 'Ej: cevans@marvels.com');
  $('#id_password1').attr('placeholder', '8 caracteres como mínimo');
  $('#id_password2').attr('placeholder', 'Repetir la contraseña escogida');
  $('#id_rut').attr('placeholder', 'Ej: 11111111-1 (sin puntos y con guión)');
  $('#id_direccion').attr('placeholder', 'Calle, n° casa o edificio, n° departamento o piso\n'
    + 'localidad o ciudad, código postal o de área\n'
    + 'estado o provincia, ciudad, país');

  // Agregar una validación por defecto para que la imagen la exija como campo obligatorio
  $.extend($.validator.messages, {
    required: "Este campo es requerido",
  });

  $('#form').validate({ 
      rules: {
        'username': {
          required: true,
        },
        'first_name': {
          required: true,
          soloLetras: true,
        },
        'last_name': {
          required: true,
          soloLetras: true,
        },
        'email': {
          required: true,
          emailCompleto: true,
        },
        'rut': {
          required: true,
          rutChileno: true,
        },
        'direccion': {
          required: true,
        },
        'password1': {
          required: true,
          minlength: 8,
        },
        'password2': {
          required: true,
          equalTo: '#id_password1'
        }
      },
      messages: {
        'username': {
          required: 'Debe ingresar un nombre de usuario',
        },
        'first_name': {
          required: 'Debe ingresar su nombre',
          soloLetras: "El nombre sólo puede contener letras y espacios en blanco",
        },
        'last_name': {
          required: 'Debe ingresar sus apellidos',
          soloLetras: "Los apellidos sólo pueden contener letras y espacios en blanco",
        },
        'email': {
          required: 'Debe ingresar su correo',
          emailCompleto: 'El formato del correo no es válido',
        },
        'rut': {
          required: 'Debe ingresar su RUT',
          rutChileno: 'El formato del RUT no es válido',
        },
        'direccion': {
          required: 'Debe ingresar su dirección',
        },
        'password1': {
          required: 'Debe ingresar una contraseña',
          minlength: 'La contraseña debe tener al menos 8 caracteres',
        },
        'password2': {
          required: 'Debe ingresar una contraseña',
          equalTo: 'Debe repetir la contraseña anterior'
        }
      },
      errorPlacement: function(error, element) {
        error.insertAfter(element); // Inserta el mensaje de error después del elemento
        error.addClass('error-message'); // Aplica una clase al mensaje de error
      },
  });

  // CREAR USUARIO DE PRUEBA: Esta función permite crear un usuario de prueba usando 
  // la API "randomuser" mientras se está programando la aplicación, pero se debe
  // quitar en la versión final.
  $('#crear_usuario_prueba').click(function(event) {
    event.preventDefault();
    $.get('https://randomuser.me/api/?results=1', // API para obtener datos de usuario al azar
      function(data){
        $.each(data.results, function(i, item) { // Recorrer las filas devueltas por la API

          $('#limpiar_formulario').click();

          $('#id_username').val(item.login.username);
          $('#id_first_name').val(item.name.first);
          $('#id_last_name').val(item.name.last);
          $('#id_email').val(item.email);
          $('#id_rut').val('11.111.111-1');
          dir = `${item.location.street.number} ${item.location.street.name}\n${item.location.city}\n${item.location.country}`;
          $('#id_direccion').val(dir);
          $('#id_subscrito').val(true);
          $('#id_imagen').val('');
          $('#id_password1').val('Duoc@123');
          $('#id_password2').val('Duoc@123');

          Swal.fire({
            title: 'Se ha creado un nuevo usuario de prueba',
            html: 
              `Se ha llenado el formulario con 
              los datos de un usuario de prueba al azar, con la password 
              por defecto: <br><br> <strong> "Duoc@123" </strong> <br><br>Si lo deseas puedes 
              seleccionar una imagen de perfil y registrar este nuevo 
              usuario presionando el botón <br><br> <strong> "Registarme" </strong>.`,
            showClass: {
              popup: 'animate__animated animate__fadeInDown'
            },
            hideClass: {
              popup: 'animate__animated animate__fadeOutUp'
            }
          })

        });
      });
  });

});