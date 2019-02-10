import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
 
Vue.use(VueAxios, axios)

new Vue({
  el: '#app',
  components: {
    'app': App
  }
})