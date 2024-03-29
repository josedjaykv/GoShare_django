$(document).ready(function() {
    // Función para mostrar mensajes de error de contraseña
    function showPasswordErrors() {
        // Obtenemos el valor de la contraseña
        var password = $("#password1").val();
        var errors = [];

        // Verificamos la longitud mínima
        if (password.length < 8) {
            errors.push("La contraseña debe tener al menos 8 caracteres.");
        }

        // Verificamos si la contraseña contiene al menos un número
        if (!/\d/.test(password)) {
            errors.push("La contraseña debe contener al menos un número.");
        }

        // Verificamos si la contraseña contiene al menos una letra mayúscula
        if (!/[A-Z]/.test(password)) {
            errors.push("La contraseña debe contener al menos una letra mayúscula.");
        }

        // Mostramos los errores
        if (errors.length > 0) {
            $("#password-error").html(errors.join("<br>"));
        } else {
            $("#password-error").html(""); // Borrar los mensajes de error si no hay errores.
        }
    }

    // Función para comprobar si las contraseñas coinciden
    function checkPasswordMatch() {
        var password1 = $("#password1").val();
        var password2 = $("#password2").val();

        if (password1 !== password2) {
            $("#password-match-error").html("Las contraseñas no coinciden.");
        } else {
            $("#password-match-error").html("");
        }
    }

    // Escuchamos el evento input en el campo de contraseña
    $("#password1").on("input", function() {
        showPasswordErrors();
        checkPasswordMatch();
    });

    // Escuchamos el evento input en el campo de confirmación de contraseña
    $("#password2").on("input", function() {
        checkPasswordMatch();
    });


    function toggleSignupButton() {
        // Obtén los campos de contraseña y los mensajes de error
        var password1 = $("#password1").val() || "";
        var password2 = $("#password2").val() || "";
        var passwordErrors = $("#password-error").text();
        var passwordMatchError = $("#password-match-error").text();

        // Verifica si hay errores en los campos
        var hasErrors = passwordErrors.trim() !== "" || passwordMatchError.trim() !== "" || password1.length < 8;

        // Habilita o deshabilita el botón según si hay errores
        $("#signup-button").prop("disabled", hasErrors);
    }

    // Escucha los eventos de entrada en los campos y los mensajes de error
    $("#password1, #password2, #password-error, #password-match-error").on("input", function() {
        toggleSignupButton();
    });

    // Ejecuta la validación al cargar la página
    toggleSignupButton();


});
