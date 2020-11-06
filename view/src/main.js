import Vue from 'vue'
import axios from './plugins/axios'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import  "./assets/css/clock/flipclock.css"
import  "./assets/css/clock/style.css"
import  "./assets/js/clock/flipclock.js"
Vue.config.productionTip = false
Vue.prototype.$ajax = axios;

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
