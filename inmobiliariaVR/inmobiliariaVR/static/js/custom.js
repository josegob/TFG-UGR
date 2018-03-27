$( document ).ready(function(){
  $(".button-collapse").sideNav();
  $('select').material_select();

    $("#form_nueva_casa").on("submit", function(event){
    event.preventDefault();
    var form = $(this).closest("form");
    var nombre_casa = $("#nombre_casa").val();

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
                         $("#row"+i).append("<div class='input-field col s3'><input placeholder='Nombre habitacion' id='nombre_habitacion' name='nombre_habitacion"+i+"' type='text' class='validate'></div><div class='form-group'><input type='file' class='form-control' id='file_to_upload' name='file_to_upload"+i+"' required></div>");
                       }

                       $("#form_habitaciones").append("<div class='row input-field col s4'><button class='waves-effect waves-light btn' type='submit'>Subir</button></div>");
                       $("#form_habitaciones").append("<input type='hidden' name='numero_ficheros' value='"+i+"'>");
                       $("#form_habitaciones").append("<input type='hidden' name='nombre_casa' value='"+nombre_casa+"'>");
                    }
                    else
                    {
                       alert(data.mensaje);
                    }
                }
        });
    });


    $("#form_habitaciones").on("submit", function(event){
        event.stopPropagation();
        event.preventDefault();
        var form = $(this).closest("form");

        $.ajax({
            type: "POST",
            url: "/appVR/upload/",
            data: form.serialize_files(),
            contentType: false,
            processData: false,
            dataType: 'json',
                success: function (data) {
                    $('#form_nueva_casa')[0].reset();
                    $('#form_habitaciones').empty();
                    alert(data.message);
                }
        });
    });

    $.fn.serialize_files = function() {
        var obj = $(this);
        var formData = new FormData();
        $.each($(obj).find("input[type='file']"), function(i, tag) {
            $.each($(tag)[0].files, function(i, file) {
                formData.append(tag.name, file);
            });
        });
        var params = $(obj).serializeArray();
        $.each(params, function (i, val) {
            formData.append(val.name, val.value);
        });
        return formData;
    };

    $("#form_seleccion_casa").on("submit", function(event){
        event.preventDefault();
        var form = $(this).closest("form");
        casa_seleccionada = $('#casa_seleccionada').val();
        $('#habitacion_seleccionada').empty();
        $('#button_habitacion').remove();

        $.ajax({
            type: "POST",
            url: "/get-habitaciones/",
            data: form.serialize(),
            dataType: 'json',
                success: function (data) {;
                    if(data.seleccionada)
                    {
                       $("#div_habitaciones").removeAttr("style");
                       $("#habitacion_seleccionada").append("<option disabled selected value>Selecciona una habitacion</option>");
                        for(i = 0; i < (data.habitaciones).length; i++)
                        {
                            $("#habitacion_seleccionada").append("<option value="+data.habitaciones[i]+">"+data.habitaciones[i]+"</option>");
                            $('select').material_select();
                        }

                        $("#div_habitaciones").append("<input type='hidden' id='casa_seleccionada_2' name='casa_seleccionada_2' value='"+casa_seleccionada+"'>");
                        $("#div_habitaciones").append("<button class='waves-effect waves-light btn' id='button_habitacion' type='submit'>Seleccionar</button>")

                    }
                    else
                    {
                        alert(data.mensaje)
                    }
                }
        });
    });

    $("#form_seleccion_habitacion").on("submit", function(event){
        event.preventDefault();
        var form = $(this).closest("form");

        $.ajax({
            type: "POST",
            url: "/get-links/",
            data: form.serialize(),
            dataType: 'json',
                success: function (data) {;
                    if(data.seleccionada)
                    {
                        $("#div_iframe").removeAttr("style");
                        $("#div_coordenadas").removeAttr("style");
                        $("#iframe_test").attr('src', 'http://127.0.0.1:8000/sample/'+data.link);

                    }
                    else
                    {
                        alert(data.mensaje)
                    }
                }
        });
    });

    $("#form_coordenadas").on("submit", function(event){
        event.preventDefault();

        var link = $("#iframe_test");
        $("#coord_x_r").val($("#coordenadas", link.contents()).attr('rotation_x'));
        $("#coord_y_r").val($("#coordenadas", link.contents()).attr('rotation_y'));
        $("#coord_z_r").val($("#coordenadas", link.contents()).attr('rotation_z'));


    });


});
