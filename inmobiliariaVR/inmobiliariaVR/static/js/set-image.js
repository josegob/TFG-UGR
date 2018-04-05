/* global AFRAME */

/**
 * Component that listens to an event, fades out an entity, swaps the texture, and fades it
 * back in.
 */

var rotation = new THREE.Vector3();
var position = new THREE.Vector3();
var distance = 8.0;


AFRAME.registerComponent('set-image', {
  schema: {
    on: {type: 'string'},
    target: {type: 'selector'},
    src: {type: 'string'},
    dur: {type: 'number', default: 300}
  },

  init: function () {
    var data = this.data;
    var el = this.el;

    this.setupFadeAnimation();

    el.addEventListener(data.on, function () {
      // Fade out image.
      var habitacion = data.src.substring(1);
      habitacion = habitacion.replace('_',' ')
      $('#hab_actual').attr('name', habitacion);
      data.target.emit('set-image-fade');
      // Wait for fade to complete.
      setTimeout(function () {
        // Set image.
        var tope = ($("#hab_actual").val());
        for(var i = 0; i < tope; i++)
        {
            var tmp = $("#links"+i).attr('name');
            if (habitacion != tmp)
                $("#links"+i).attr('visible', false);
            else
                $("#links"+i).attr('visible', true);
        }
        data.target.setAttribute('material', 'src', data.src);
      }, data.dur);
    });

  },

  /**
   * Setup fade-in + fade-out.
   */
  setupFadeAnimation: function () {
    var data = this.data;
    var targetEl = this.data.target;

    // Only set up once.
    if (targetEl.dataset.setImageFadeSetup) { return; }
    targetEl.dataset.setImageFadeSetup = true;

    // Create animation.
    targetEl.setAttribute('animation__fade', {
      property: 'material.color',
      startEvents: 'set-image-fade',
      dir: 'alternate',
      dur: data.dur,
      from: '#FFF',
      to: '#000'
    });
  }
});

AFRAME.registerComponent('camera-listener', {
  tick: function () {
    var cameraEl = this.el.sceneEl.camera.el;
    var position = cameraEl.getAttribute('position');
    var rotation = cameraEl.getAttribute('rotation');
    //console.log(rotation);


  }
});

AFRAME.registerComponent('rotation-reader', {
      tick: function () {
        rotation = this.el.getAttribute('rotation');
        position = this.el.getAttribute('position');
        num_t = $("#hab_actual").attr('value')

        $("#coordenadas").attr('rotation_x', rotation.x);
        $("#coordenadas").attr('rotation_y', rotation.y);
        $("#coordenadas").attr('rotation_z', rotation.z);

      }
});

AFRAME.registerComponent('rk', {
      tick: function () {
        var worldPos = new THREE.Vector3();
        worldPos.setFromMatrixPosition(this.el.object3D.matrixWorld);
        var posision = new THREE.Vector3();
        posision = new THREE.Vector3(worldPos.x-position.x, worldPos.y-position.y, worldPos.z - position.z);
        posision = posision.normalize();
        posision = new THREE.Vector3(posision.x*distance, posision.y*distance, posision.z*distance);

        //console.log(posision);
        $("#coordenadas").attr('position_x', posision.x);
        $("#coordenadas").attr('position_y', posision.y);
        $("#coordenadas").attr('position_z', posision.z);


      }
});

AFRAME.registerComponent('aaa', {
      tick: function () {
        name = this.el.getAttribute('material');
            //console.log(name);



      }
});