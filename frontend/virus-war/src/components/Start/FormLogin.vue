<template>
  <form id="form-login" @submit.prevent="signIn()">
    <div class="auth-error"> {{ non_field_errors }} </div>

    <base-input type="text" name="username" placeholder="Имя пользователя"/>
    <div class="auth-error"> {{ username_errors }} </div>

    <base-input type="password" name="password" placeholder="Пароль"/>
    <div class="auth-error"> {{ password_errors }} </div>

    <button class="auth-button"> Войти </button>
    <!-- {{info}} -->
  </form>
</template>

<script>
import BaseInput from '../BaseInput.vue'

export default {
  name: 'FormLogin',
  components: {
    BaseInput,
  },
  data() {
    return {
      non_field_errors: '',
      username_errors: '',
      password_errors: '', 
      info: ""
    }
  },
  methods: {
    signIn() {
      this.info = 'registered';
    }
  },
}
</script>

<style scoped>
form {
  margin-top: 7%;
  display: flex;
  flex-direction: column;
}
</style>