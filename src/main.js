import Vue from 'vue'
import axios from './plugins/axios'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import echarts from 'echarts'
import "./assets/scrollbar.css"
Vue.prototype.$echarts = echarts
Vue.config.productionTip = false

new Vue({
    vuetify,
    axios,
    render: h => h(App)
}).$mount('#app')