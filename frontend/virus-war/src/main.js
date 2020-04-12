import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import axios from 'axios'

import PageStart from '@/components/Start/PageStart'
import PageLobby from '@/components/Lobby/PageLobby'
import PageRoom from '@/components/Room/PageRoom'


const router = new VueRouter({
  routes: [
    { path: '/', name: 'root', component: PageStart},
    { path: '/lobby', name: 'lobby', component: PageLobby },
    { path: '/room/:id', name: 'room', component: PageRoom, props: true },
  ]
})

Vue.prototype.$axios = axios.create({
  baseURL:  'http://0.0.0.0:8000' // 
})

if (localStorage.getItem('auth_token')) {
  Vue.prototype.$axios.defaults.headers.common['Authorization'] = "Token " + localStorage.getItem('auth_token');
}
Vue.use(VueRouter)
Vue.config.productionTip = false

new Vue({
  router: router,
  render: h => h(App),
}).$mount('#app')
