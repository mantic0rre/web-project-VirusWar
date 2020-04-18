<template>
  <div id="start-page">
    <div class="description">
      <div>
      <p> Стратегическая игра, <br>имитирующая развитие колоний вирусов, <br>
          которые развиваются сами и уничтожают друг друга. </p>
      </div>
      <slider-anima class="slider"/>
    </div>

    <div class="forms">
      <form-login @setusername='setusername'/>
      <form-register/>
    </div>    
    {{user}}
  </div>
</template>

<script>
import FormLogin from './FormLogin.vue'
import FormRegister from './FormRegister.vue'
import SliderAnima from './SliderAnima.vue';

export default {
  name: 'PageStart',
  components: {
    FormLogin, 
    FormRegister,
    SliderAnima, 
  },
  
  methods :{
    setusername(username) {
      this.$emit('sendusername', username);
    },
    log_out(){
      this.$axios.post('/api/auth/token/logout/');
      localStorage.clear();  
      delete this.$axios.defaults.headers.common["Authorization"];
    }
  },
  created() {
    this.$emit('sendusername', null);
    this.log_out();
  }
}
</script>

<style scoped>
#start-page {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}
.description {
  flex: 2;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
}
.forms {
  flex: 1;
  padding-right: 8%;
}
.slider {
  align-self: center;
}
@media (max-width: 650px) {
  #start-page {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    font-size: 100%;
    padding: 0px;
  }
  .description, .forms {
    padding: 0vh;
    width: 100%;
  }
}
</style>