$( document ).ready(function(){
  $(".button-collapse").sideNav();

    $("#form_nueva_casa").on("submit", function(event){
    event.preventDefault();
    var form = $(this).closest("form");

        $.ajax({
            type: "POST",
            url: "/appVR/nueva-casa/",
            data: form.serialize(),
            dataType: 'json',
                success: function (data) {
                    if (data.creado) {
                       $('#form_habitaciones').empty();
                       for(i = 0; i < data.habitaciones; i++)
                       {
                         $("#form_habitaciones").append("<div class='row' id=row"+i+" </div>");
                       }
                       for(i = 0; i < data.habitaciones; i++)
                       {
                         $("#row"+i).append("<div class='input-field col s3'><input placeholder='Nombre habitacion' id='nombre_habitacion' name='nombre_habitacion' type='text' class='validate'></div><div class='input-field col s3'><input placeholder='Imagen habitacion' id='imagen_habitacion' name='imagen_habitacion' type='text' class='validate'></div>");
                       }
                    }
                    else
                    {
                       alert(data.mensaje);
                    }
                }
        });
    });

});
