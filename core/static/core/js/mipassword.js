$(document).ready(function() {

  var label = $('label[for="id_old_password"]');
  label.text('Contraseña actual');
  $('#id_old_password').attr('placeholder', 'Ingesa tu contraseña actual');
  $('#id_new_password1').attr('placeholder', '8 caracteres como mínimo');
  $('#id_new_password2').attr('placeholder', 'Repetir la contraseña escogida');

  $('#form').validate({ 
      rules: {
        'old_password': {
          required: true,
        },
        'new_password1': {
          required: true,
        },
        'new_password2': {
          required: true,
          equalTo: '#id_new_password1'
        },
      },
      messages: {
        'old_password': {
          required: 'Debe ingresar su contraseña actual',
        },
        'new_password1': {
          required: 'Debe ingresar una nueva contraseña',
        },
        'new_password2': {
          required: 'Debe ingresar una nueva contraseña',
          equalTo: 'La nueva contraseña y su confirmación deben ser iguales',
        },
      },
      errorPlacement: function(error, element) {
        error.insertAfter(element); // Inserta el mensaje de error después del elemento
        error.addClass('error-message'); // Aplica una clase al mensaje de error
      },
  });

});
