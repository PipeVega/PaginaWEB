$(document).ready(function () {

    $('[data-toggle="tooltip"]').tooltip();

    if ($('#tabla-principal').length > 0) {
        var table = new DataTable('#tabla-principal', {
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
            }
        });
      }
    
    if ($('#limpiar_formulario').length > 0) {
    $('#limpiar_formulario').click(function(event) {
        $("#form").validate().resetForm();
    });
    }

    if ($('#id_imagen').length > 0) {
        $("label[for='id_imagen']").hide();
        $('#id_imagen').insertAfter('#cuadro-imagen');
        $("#id_imagen").css("opacity", "0");
        $("#id_imagen").css("height", "0px");
        $("#id_imagen").css("width", "0px");
        $('#form').removeAttr('style');
    }
    
    if ($('#id_subscrito').length > 0) {
        $('#id_subscrito').wrap('<div class="row"></div>');
        $('#id_subscrito').wrap('<div class="col-sm-1" id="checkbox-subscrito"></div>');
        $('#checkbox-subscrito').after('<div id="help_text_id_subscrito" class="col-sm-11"></div>');
        $('#help_text_id_subscrito').text(`Deseo subscribirme con un aporte
          de $3.000 mensuales a la fundación "Help a Brother" y obtner un 
          5% de descuento en todas mis compras.`);
    }

    if ($('#id_imagen').length > 0) {
        $('#id_imagen').change(function() {
          var input = this;
          if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
              $('#cuadro-imagen').attr('src', e.target.result).show();
            };
            reader.readAsDataURL(input.files[0]);
          }
        });
    }

    if ($('#carousel-indicators').length > 0) {
        const myCarouselElement = document.querySelector('#carousel-indicators');
        const carousel = new bootstrap.Carousel(myCarouselElement, {
          interval: 10,
          touch: false
        });
      };

    $.validator.addMethod("rutChileno", function(value, element) {
        value = value.replace(/[.-]/g, "");

        if (value.length < 8 || value.length > 9) {
            return false;
        }

        var validChars = "0123456789K";
        var lastChar = value.charAt(value.length - 1).toUpperCase();
        if (validChars.indexOf(lastChar) == -1) {
            return false;
        }

        var rut = parseInt(value.slice(0, -1), 10);
        var factor = 2;
        var sum = 0;
        var digit;
        while (rut > 0) {
            digit = rut % 10;
            sum += digit * factor;
            rut = Math.floor(rut / 10);
            factor = factor === 7 ? 2 : factor + 1;
        }
        var dv = 11 - (sum % 11);
        dv = dv === 11 ? "0" : dv === 10 ? "K" : dv.toString();

        return dv === lastChar;
        }, "Por favor ingrese un RUT válido.");

        if(document.getElementById('id_rut')){
            document.getElementById('id_rut').addEventListener('keyup', function(e) {
            e.target.value = e.target.value.toUpperCase();
            for (let i = 0; i < e.target.value.length; i++) {
                const caracter = e.target.value[i];
                if (!"0123456789kK-".includes(caracter)) {
                e.target.value = e.target.value.replace(caracter, "");
                }
            }
        });
    }
    
    $.validator.addMethod("emailCompleto", function (value, element) {
        var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z\-0-9]{2,}))$/;
        return regex.test(value);
    }, 'El formato del correo no es válido');

    $.validator.addMethod("soloLetras", function (value, element) {
        var regex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑçÇ\s]+$/;
        return regex.test(value);
    }, "Sólo se permiten letras y espacios en blanco.");    

    $.validator.addMethod("inList", function(value, element, param) {
        return $.inArray(value, param) !== -1;
      }, "Por favor, selecciona un valor válido.");
    
    $("#formulario-registro").validate({
        rules: {
            rut: {
                required: true,
                rutChileno: true
            },
            nombres: {
                soloLetras: true,
                required: true,
            },
            apellidos: {
                soloLetras: true,
                required: true,
            },
            correo: {
                required: true,
                emailCompleto: true,
            },
            direccion: {
                minlength: 5,
                required: true,
            },
            password: {
                required: true,
                minlength: 5,
                maxlength: 15,
            },
            confirm_password: {
                required: true,
                minlength: 5,
                maxlength: 15,
                equalTo: "#password",
            },
        },
        messages: {
            rut: {
                required: "Este campo es obligatorio",
                rutChileno: "El formato del rut no es válido",
            },
            nombres: {
                required: "Este campo es obligatorio",
                soloLetras: "Este campo sólo acepta letras",
            },
            apellidos: {
                required: "Este campo es obligatorio",
                soloLetras: "Este campo sólo acepta letras",
            },
            correo: {
                required: "Este campo es obligatorio",
                emailCompleto: "El correo no cumple con el formato válido",
            },
            direccion: {
                required: "Este campo es obligatorio",
                minlength: "La dirección debe tener al menos 5 caracteres.",
            },
            password: {
                required: "Este campo es obligatorio",
                minlength: "La contraseña debe tener al menos 5 caracteres.",
                maxlength: "La contraseña debe tener menos de 15 caracteres.",
            },
            confirm_password: {
                required: "Este campo es obligatorio",
                minlength: "La contraseña debe tener al menos 5 caracteres.",
                maxlength: "La contraseña debe tener menos de 15 caracteres.",
                equalTo: "Las contraseñas no coinciden",
            },
        },
    });

    $("#formulario-m-usuarios").validate({
        rules: {
            idUsuario: {
                required: true,
            },
            tipoUsuario: {
                required: true,
            },
            rut: {
                required: true,
                rutChileno: true
            },
            nombres: {
                soloLetras: true,
                required: true,
            },
            apellidos: {
                soloLetras: true,
                required: true,
            },
            correo: {
                required: true,
                emailCompleto: true,
            },
            direccion: {
                minlength: 5,
                required: true,
            },
            password: {
                required: true,
                minlength: 5,
                maxlength: 15,
            },
        },
        messages: {
            idUsuario: {
                required: "Este campo es obligatorio",
            },
            tipoUsuario: {
                required: "Este campo es obligatorio",
            },
            rut: {
                required: "Este campo es obligatorio",
                rutChileno: "El formato del rut no es válido",
            },
            nombres: {
                required: "Este campo es obligatorio",
                soloLetras: "Este campo sólo acepta letras",
            },
            apellidos: {
                required: "Este campo es obligatorio",
                soloLetras: "Este campo sólo acepta letras",
            },
            correo: {
                required: "Este campo es obligatorio",
                emailCompleto: "El correo no cumple con el formato válido",
            },
            direccion: {
                required: "Este campo es obligatorio",
                minlength: "La dirección debe tener al menos 5 caracteres.",
            },
            password: {
                required: "Este campo es obligatorio",
                minlength: "La contraseña debe tener al menos 5 caracteres.",
                maxlength: "La contraseña debe tener menos de 15 caracteres.",
            },
        },

        errorPlacement: function (error, element) {
            if (element.attr("name") === "tipoUsuario") {
                error.appendTo($(".tipoUsuario").append("<br>"));
            } else if (element.attr("name") === "password") {
                error.insertAfter(element.next("button"));
                error.css("margin-left", "10px");
            } else {
                error.insertAfter(element);
            }
        },
    });

    $("#formulario-m-productos").validate({
        rules: {
            categoria: {
                required: true
            },
            nombre: {
                required: true,
                minlength: 3,
            },
            descripcion: {
                required: true,
                minlength: 20,
                maxlength: 400,
            },
            precio: {
                required: true,
                number: true,
                min: 0,
            },
            descuento_subscriptor: {
                required: true,
                number: true,
                min: 0,
                max: 100,
            },
            descuento_oferta: {
                required: true,
                number: true,
                min: 0,
                max: 100,
            },
            imagen: {
                required: true,
            },
        },
        messages: {
            categoria: {
                required: "Este campo es obligatorio"
            },
            nombre: {
                required: "Este campo es obligatorio",
                minlength: "El nombre debe tener al menos 3 carácteres",
            },
            descripcion: {
                required: "Este campo es obligatorio",
                minlength: "La descripción debe tener al menos 20 carácteres",
                maxlength: "La descripción debe tener menos de 400 carácteres",
            },
            precio: {
                required: "Este campo es obligatorio",
                number: "El precio debe ser un número",
                min: "El precio debe ser mayor o igual a 0",
            },
            descuento_subscriptor: {
                required: "Este campo es obligatorio",
                number: "El descuento de subscriptor debe ser un número",
                min: "El descuento de subscriptor debe ser mayor o igual a 0",
                max: "El descuento de subscriptor debe ser mayor o igual a 100",
            },
            descuento_oferta: {
                required: "Este campo es obligatorio",
                number: "El descuento por oferta debe ser un número",
                min: "El descuento por oferta debe ser mayor o igual a 0",
                max: "El descuento por oferta debe ser mayor o igual a 100",
            },
            imagen: {
                required: "Este campo es obligatorio",
            },
        },

        errorPlacement: function (error, element) {
            if (element.attr("name") === "tipoUsuario") {
                error.appendTo($(".tipoUsuario").append("<br>"));
            } else if (element.attr("name") === "password") {
                error.insertAfter(element.next("button"));
                error.css("margin-left", "10px");
            } else {
                error.insertAfter(element);
            }
        },
    });

    $("#formulario-m-bodega").validate({
        rules: {
            categoria: {
                required: true,
            },
            nombreCategoria: {
                required: true,
            },
            cantidad: {
                required: true,
                soloNumeros: true
            },
        },

        messages: {
            categoria: {
                required: "Este campo es obligatorio",
            },
            nombreCategoria: {
                required: "Este campo es obligatorio",
            },
            cantidad: {
                required: "Este campo es obligatorio",
                soloNumeros: "Este campo sólo acepta números"
            },
        },
    });

    $("#formulario-mis-datos").validate({
        rules: {
            rut: {
                required: true,
                rutChileno: true,
            },
            nombres: {
                required: true,
                soloLetras: true,
            },
            apellidos: {
                required: true,
                soloLetras: true,
            },
            correo: {
                required: true,
                emailCompleto: true,
            },
            direccion: {
                required: true,
                minlength: 5,
            },
            password: {
                required: true,
                minlength: 5,
                maxlength: 15,
            },
            confirm_password: {
                required: true,
                minlength: 5,
                maxlength: 15,
                equalTo: "#password",
            },
        },
        messages: {
            rut: {
                required: "Este campo es obligatorio",
                rutChileno: "El formato del RUT no es válido.",
            },
            nombres: {
                required: "Este campo es obligatorio",
                soloLetras: "Este campo sólo acepta letras",
            },
            apellidos: {
                required: "Este campo es obligatorio",
                soloLetras: "Este campo sólo acepta letras",
            },
            correo: {
                required: "Este campo es obligatorio",
                emailCompleto: "Por favor, ingrese un correo electrónico válido.",
            },
            direccion: {
                required: "Este campo es obligatorio",
                minlength: "La dirección debe tener al menos 5 caracteres.",
            },
            password: {
                required: "Este campo es obligatorio",
                minlength: "La contraseña debe tener al menos 5 caracteres.",
                maxlength: "La contraseña debe tener menos de 15 caracteres.",
            },
            confirm_password: {
                required: "Este campo es obligatorio",
                minlength: "La contraseña debe tener al menos 5 caracteres.",
                maxlength: "La contraseña debe tener menos de 15 caracteres.",
                equalTo: "Las contraseñas no coinciden.",
            },
        },
    });

    $("#formulario-ingreso").validate({
        rules: {
            username: {
                required: true,
            },
            password: {
                required: true,
                minlength: 5,
                maxlength: 15,
            },
        },
        messages: {
            username: {
                required: "Este campo es obligatorio",
            },
            password: {
                required: "Este campo es obligatorio",
                minlength: "La contraseña debe tener al menos 5 caracteres.",
                maxlength: "La contraseña debe tener menos de 15 caracteres.",
            },
        },
    });
});
