$(document).ready(function() {

  // Asignar placeholders para ayudar a los usuarios
  $('#id_username').attr('placeholder', 'Ej: cgomezv, cevans, sjohasson');
  $('#id_password').attr('placeholder', 'Ingesa tu contraseña actual');

  $('#form').validate({ 
      rules: {
        'username': {
          required: true,
        },
        'password': {
          required: true,
        },
      },
      messages: {
        'username': {
          required: 'Debe ingresar un nombre de usuario',
        },
        'password': {
          required: 'Debe ingresar una contraseña',
        },
      },
      errorPlacement: function(error, element) {
        error.insertAfter(element); // Inserta el mensaje de error después del elemento
        error.addClass('error-message'); // Aplica una clase al mensaje de error
      },
  });

  $('#user-select').change(function() {
    var username = $(this).val();
    var password = 'Duoc@123';
    if ('cmontenegro ejara msaavedra afernandez bjana ahernandez alejandrosuper super'.includes(username)) {
      password = '123';
    };
    $('#id_username').val(username);
    $('#id_password').val(password);
  });

});
