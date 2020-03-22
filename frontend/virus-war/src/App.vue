<template>
  <div id="app">
    <site-header :user="username" @unreg="unreg" @modalShow="showModal"/>
    <main>
      <router-view @sendusername="sendusername"/>
    </main>   
    <modal-rules v-show="isModalVisible" @close="closeModal"/> 
  </div>
</template>

<script>
import SiteHeader from './components/SiteHeader.vue'
import ModalRules from './components/ModalRules.vue';

export default {
  name: 'App',
  components: {
    SiteHeader,
    ModalRules
  },
  data () {
    return { 
      isModalVisible: false,
      username: 'milly',
    };
  },
  methods: {
    showModal() { this.isModalVisible = true; },
    closeModal() { this.isModalVisible = false; },
    sendusername(username) { this.username = username},
  },
}
</script>

<style>
div, header {
  border: 0px solid black;
}
body {
  margin: 0px;
  text-align: center;
  height: 100vh;
  background: radial-gradient(50% 50% at 50% 50%, #96AFD1 0%, #3C73C5 100%);
  font-family: Comic Sans MS, Comic Sans, cursive;
  font-size: 120%;
  color: white;
  display: flex;
  flex-direction: column;
  
}
main, header{
  border: 0.0px solid black;
  /*max-width: 1500px;*/
  margin: auto;
}
main {
  flex: auto;
  overflow: auto;  
}
.auth-button {
  background-color: #003884;
  border: 1.6px solid white;
  border-radius: 100px 100px 100px 100px;
  margin: 0.5em auto 0.5em auto ; 
  width: 75%;
  min-width: 200px;
  height: 40px;
  font-family: Comic Sans MS, Comic Sans, cursive;
  font-size: 100%;
  color: white;
}


.auth-button, #howplay, .btn-close, .btn-i-know {
  cursor: pointer;
  outline: none;
}

.auth-button:hover { /*поведение чекбокса при наведении*/
  color: #91eeff;
  border: 1.6px solid #91eeff!important; /*выполнение в любом случае*/
}

.auth-error {
  font-size: 80%;
  color: #c8ff00;
}
@font-face {
    font-family: 'Pecita';
    src: url('~@/assets/fonts/pecita/pecita.woff2') format('woff2'), 
         url('~@/assets/fonts/pecita/pecita.woff') format('woff'), 
         url('~@/assets/fonts/pecita/pecita.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}
</style>