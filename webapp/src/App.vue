<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <h3 class="navbar-brand">tylko</h3>
      <div class="btn-group mr-sm-2" role="group">
        <button type="button" class="btn btn-warning" @click="groupByTouch">Pokaż styczne</button>
        <button type="button" class="btn btn-warning" @click="groupByThickness">Pokaż podobne</button>
        <button type="button" class="btn btn-warning" @click="showAll">Pokaż wszystkie</button>
      </div>
    </nav>
  </div>
</template>

<script>
const THREE = require('three')
const OrbitControls = require('three-orbitcontrols')

export default {
  name: 'app',
  data () {
    return {
      initialData: null,
      allBoxes: [],
      attachedBoxes: [],
      thicknessBoxes: [],
      scene: null,
      renderer: null,
      camera: null,
      controls: null,
    }
  },
  mounted() {
    this.initViewPort()
    this.setCameraPosition()
    this.setLight(500, 1)
    this.loadGeometry()
    this.update()
  },
  methods: {
    groupByThickness(){
      this.clearTheScene()
      for (let index = 0; index < this.thicknessBoxes.length; index++) {
        const box = this.thicknessBoxes[index]
        this.scene.add(box)
      }
      this.setLight(500, 1)
      this.update()
    },
    groupByTouch(){
      this.clearTheScene()
      for (let index = 0; index < this.attachedBoxes.length; index++) {
        const box = this.attachedBoxes[index]
        this.scene.add(box)
      }
      this.setLight(500, 1)
      this.update()
    },
    showAll(){
      this.clearTheScene()
      for (let index = 0; index < this.allBoxes.length; index++) {
        const box = this.allBoxes[index]
        this.scene.add(box)
      }
      this.setLight(500, 1)
      this.update()
    },
    initViewPort(){
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 )
      this.renderer = new THREE.WebGLRenderer()
      this.renderer.setSize( window.innerWidth, window.innerHeight )
      this.controls = new OrbitControls( this.camera, this.renderer.domElement )
      document.body.appendChild( this.renderer.domElement )
      //this.scene.fog = new THREE.FogExp2(0xffffff, 0.05)
      this.renderer.setClearColor('rgb(80, 80, 80)')
    },
    setCameraPosition(){
      this.camera.position.z = 200;
      this.camera.position.y = 50;
      this.camera.position.x = 50;
    },
    setLight(distance, intensity){      
      let light1 = new THREE.PointLight(0Xffffff, intensity)
      let light2 = new THREE.PointLight(0Xffffff, intensity)
      let light3 = new THREE.PointLight(0Xffffff, intensity)
      let light4 = new THREE.PointLight(0Xffffff, intensity)
      let light5 = new THREE.PointLight(0Xffffff, intensity)
      light1.position.y = distance
      light2.position.x = distance
      light3.position.z = distance
      light4.position.x = distance * (-1)
      light5.position.z = distance * (-1)
      this.scene.add(light1)
      this.scene.add(light2)
      this.scene.add(light3)
      this.scene.add(light4)
      this.scene.add(light5)
    },
    update() {
      this.renderer.render( this.scene, this.camera );
      this.controls.update()

      requestAnimationFrame(() => {
        this.update()
      })
    },
    loadGeometry() {
      this.axios.get('/boxes').then((response) => {
        this.initialData = response.data
        console.log(response.data)
        for (var i = 0; i < response.data.all.length; i++) {
            let boxGeometry = this.getBoxGeometry(response.data.all[i], 'rgb(150, 150, 150)')
            this.scene.add(boxGeometry)
            this.allBoxes.push(boxGeometry)
        }
        for (var i = 0; i < response.data.thickness.length; i++) {
            let boxGeometry = this.getBoxGeometry(response.data.thickness[i], 'rgb(255,127,80)')
            this.thicknessBoxes.push(boxGeometry)
        }
        for (var i = 0; i < response.data.attached.length; i++) {
            let boxGeometry = this.getBoxGeometry(response.data.attached[i], 'rgb(30,144,255)')
            this.attachedBoxes.push(boxGeometry)
        }
      })
    },
    getBoxGeometry(element, color_rgb) {
      var geometry = new THREE.BoxGeometry( element.width, element.height, element.depth )
      var material = new THREE.MeshPhongMaterial( {color: color_rgb} );
      var cube = new THREE.Mesh( geometry, material )
      cube.position.x = element['position'].x
      cube.position.y = element['position'].y
      cube.position.z = element['position'].z
      return cube;
    },
    clearTheScene() {
      console.log(this.scene.children)
      for( var i = this.scene.children.length - 1; i >= 0; i--) { 
        let obj = this.scene.children[i];
        this.scene.remove(obj);
      }
    }
  },
}
</script> 

<style lang="scss">

</style>
