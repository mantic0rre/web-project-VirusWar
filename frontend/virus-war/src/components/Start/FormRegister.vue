<template>
  <form id="form-register" @submit.prevent="signUp()">
    <div id="title">
      <div id='first-game'> Впервые в игре? </div>
      <div id="fast-reg"> Быстрая регистрация </div>
    </div>

    <base-input v-model="username" type="text" name="username" placeholder="Имя пользователя"/>
    <div class="auth-error"> {{ username_errors }} </div>
    
    <base-input v-model="password" type="password" name="password" placeholder="Пароль"/>
    <div class="auth-error"> {{ password_errors }} </div> 

    <base-input v-model="password_repeat" type="password" placeholder="Повторите пароль"/>
    <div class="auth-error"> {{ password_repeat_err }} </div>  

    <button class="auth-button"> Зарегистрироваться </button>
    <div v-show="is_registered"> Вы успешно зарегистрировались!<br>Пожалуйста, введите свои данные для входа. </div> 
    <div class="auth-error"> {{ non_field_errors }} </div> 
  </form>
</template>

<script>
import BaseInput from '../BaseInput.vue'

export default {
  name: 'FormRegister',
  components: {
    BaseInput
  },
  data() { 
    return { 
      info: '',
      is_registered: false,
      username: '',
      password: '',
      password_repeat: '',
      password_repeat_err: '',
      non_field_errors: '',
      username_errors: '',
      password_errors: ''
    }
  },
  methods: {
    signUp() {
      this.is_registered = true;
    }
  },
}
</script>

<style scoped>
#form-register {
  display: flex;
  flex-direction: column;
  margin-top: 7%;
}
#title {
  display: flex;
  flex-direction: column;
}
#fast-reg {
  font-size: 70%;
  margin: 0.5em 0;
}
</style>