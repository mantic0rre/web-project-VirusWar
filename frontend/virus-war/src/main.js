import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import axios from 'axios'

import PageStart from '@/components/Start/PageStart'

const router = new VueRouter({
  routes: [
    { path: '/', name: 'root', component: PageStart},
  ]
})

Vue.prototype.$axios = axios.create({
  baseURL: 'http://0.0.0.0:8000' //   
})

Vue.use(VueRouter)
Vue.config.productionTip = false

new Vue({
  router: router,
  render: h => h(App),
}).$mount('#app')
