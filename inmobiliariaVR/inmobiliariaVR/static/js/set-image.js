/* global AFRAME */

/**
 * Component that listens to an event, fades out an entity, swaps the texture, and fades it
 * back in.
 */

var rotation = new THREE.Vector3();
var position = new THREE.Vector3();
var distance = 8.0;

function vector3ToSphericalCoords(vector) {
  var phi = Math.acos(vector.y / Math.sqrt(vector.x * vector.x + vector.y * vector.y + vector.z * vector.z));
  var theta = Math.atan2(vector.x, vector.z);
  return {
    longitude: theta < 0 ? -theta : (Math.PI * 2.0) - theta,
    latitude: (Math.PI / 2.0) - phi
  };
};

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
      data.target.emit('set-image-fade');
      // Wait for fade to complete.
      setTimeout(function () {
        // Set image.
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
        var asaad = vector3ToSphericalCoords(rotation);
        //console.log(position);
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

        console.log(posision);


      }
});