$( document ).ready(function(){
  $(".button-collapse").sideNav();
  $('select').material_select();
  var casa_seleccionada;
  var habitacion_select;
  var array_habitaciones = new Array();

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
                    if(data.creada)
                    {
                        $('#form_nueva_casa')[0].reset();
                        $('#form_habitaciones').empty();
                        alert(data.message);
                        $("#tabla_casas").empty();

                        for(i = 0; i < (data.casas).length; i++)
                        {

                            $("#tabla_casas").append("<tr><td>"+data.casas[i]+"</td><td id='"+data.casas[i]+"'><button id='editar' class='btn waves-effect waves-light'>Editar</button></td><td name='"+data.casas[i]+"'><button id='eliminar' class='btn waves-effect waves-light'>Eliminar</button></td></tr>");
                            $( ".boton_tabla" ).on( "click", botonTabla );
                        }

                        window.location.replace("edicion-habitaciones/"+data.casa_creada+"/");
                    }
                    else
                    {
                        alert(data.message);
                    }

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
                            array_habitaciones.push(data.habitaciones[i])
                            var tmp = data.habitaciones[i]
                            $("#habitacion_seleccionada").append("<option value='"+data.habitaciones[i]+"'>"+data.habitaciones[i]+"</option>");
                            $('select').material_select();
                        }

                        $("#div_habitaciones").append("<input type='hidden' id='casa_seleccionada_2' name='casa_seleccionada_2' value='"+casa_seleccionada+"'>");

                    }
                    else
                    {
                        alert(data.mensaje);
                    }
                }
        });
    });

    $("#form_seleccion_habitacion").on("submit", function(event){
        event.preventDefault();
        habitacion_select = $('#habitacion_seleccionada').parent(["0"]).children()[1].value;
        console.log(habitacion_select);
        var form = $(this).closest("form");
        $('#habitacion_seleccionada_2').empty();

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
                        $("#form_coordenadas").append("<input type='hidden' id='casa_seleccionada_3' name='casa_seleccionada_3' value='"+casa_seleccionada+"'>");
                        $("#form_coordenadas").append("<input type='hidden' id='habitacion_select_2' name='habitacion_select_2' value='"+habitacion_select+"'>");
                        $("#iframe_test").attr('src', 'http://127.0.0.1:8000/sample/'+data.link);

                        $("#habitacion_seleccionada_2").append("<option disabled selected value>Selecciona una habitacion</option>");
                        for(i = 0; i < (data.habitaciones).length; i++)
                        {
                            $("#habitacion_seleccionada_2").append("<option value='"+data.habitaciones[i]+"'>"+data.habitaciones[i]+"</option>");
                            $('select').material_select();
                        }

                    }
                    else
                    {
                        alert(data.mensaje)
                    }
                }
        });
    });

    $("#coor_previas").on("click", function(event){
        event.preventDefault();

        var link = $("#iframe_test");
        $("#coord_x_r").val($("#coordenadas", link.contents()).attr('rotation_x'));
        $("#coord_y_r").val($("#coordenadas", link.contents()).attr('rotation_y'));
        $("#coord_z_r").val($("#coordenadas", link.contents()).attr('rotation_z'));

        $("#coord_x_p").val($("#coordenadas", link.contents()).attr('position_x'));
        $("#coord_y_p").val($("#coordenadas", link.contents()).attr('position_y'));
        $("#coord_z_p").val($("#coordenadas", link.contents()).attr('position_z'));


    });

    $("#form_coordenadas").on("submit", function(event){
        event.preventDefault();
        var form = $(this).closest("form");

        $.ajax({
            type: "POST",
            url: "/appVR/guardar-boton/",
            data: form.serialize(),
            dataType: 'json',
                success: function (data) {;
                    if(data.creado)
                    {
                        $('#form_coordenadas')[0].reset();
                        alert(data.mensaje);
                    }
                    else
                    {
                        alert(data.mensaje);
                    }
                }
        });


    });

    $("#form_seleccion_habitacion_previa").on("submit", function(event){
        event.preventDefault();
        var form = $(this).closest("form");
        habitacion_select = $('#habitacion_seleccionada').val();

        $.ajax({
            type: "POST",
            url: "/get-links/",
            data: form.serialize(),
            dataType: 'json',
                success: function (data) {;
                    if(data.seleccionada)
                    {
                        $("#div_iframe").removeAttr("style");
                        $("#pantalla_completa").removeAttr("style");
                        $("#iframe_test").attr('src', 'http://127.0.0.1:8000/sample-buttons/'+data.link+'/'+casa_seleccionada+'/'+habitacion_select);
                        $("#href_button").attr('href', 'http://127.0.0.1:8000/sample-buttons/'+data.link+'/'+casa_seleccionada+'/'+habitacion_select);

                    }
                    else
                    {
                        alert(data.mensaje)
                    }
                }
        });
    });

    function botonTabla() {
      var casa = (($(this).closest("td")).attr('name'));
      var accion = ($(this).attr('id'));
      if (accion == 'eliminar')
      {
        $.ajax({
            type: "POST",
            url: "/appVR/eliminar-casa/",
            data: {seleccion: casa},
            dataType: 'json',
                success: function (data) {;
                    $("#tabla_casas").empty();

                    for(i = 0; i < (data.casas).length; i++)
                    {
                        $("#tabla_casas").append("<tr><td>"+data.casas[i]+"</td><td name='"+data.casas[i]+"'><button id='editar' class='btn waves-effect waves-light boton_tabla'>Editar</button></td><td name='"+data.casas[i]+"'><button id='eliminar' class='btn waves-effect waves-light boton_tabla'>Eliminar</button></td></tr>");
                        $( ".boton_tabla" ).on( "click", botonTabla );
                    }

                }
        });
      }
      else
      {
        window.location.replace("edicion-habitaciones/"+casa+"/");
      }
    }

    $( ".boton_tabla" ).on( "click", botonTabla );
    $( ".fin_edicion" ).click(function() {
      window.location.replace("/");
    });

    //var d = ($("#iframe_test").attr('src')
    //var asd = $.get(d);
    //asd.responseText;

});
