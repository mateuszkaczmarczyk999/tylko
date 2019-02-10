<template>
  <div id="app">
    Load File
  </div>
</template>

<script>
const THREE = require('THREE')

export default {
  name: 'app',
  data () {
    return {
      msg: ''
    }
  },
  mounted() {
    this.refreshMessage()

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );

    var renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );

    var geometry = new THREE.BoxGeometry( 1, 1, 1 );
    var material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
    var cube = new THREE.Mesh( geometry, material );
    scene.add( cube );

    camera.position.z = 5;

    renderer.render( scene, camera );
  },
  methods: {
    refreshMessage() {
      this.$http.get('/boxes').then((response) => {
        this.msg = response.data;
        console.log(this.msg)
      });
    }
  },
}
</script>

<style lang="scss">

</style>
