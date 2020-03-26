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
      let form = document.getElementById("form-login");
      let form_data = new FormData(form);
      let username = '';
      // для отображения ошибки с пустым полем
      for(let pair of form_data.entries()) {
        pair[1] ? null: form_data.set([pair[0]], ' ');
        if (pair[0] === 'username')
          username = pair[1];
      }      
      
      this.$axios.post('/api/auth/token/login/', form_data)
      .then(response => (localStorage.setItem("auth_token", response.data.auth_token),
                         this.$emit('setusername', username),
                         this.$router.push({name: 'lobby'},
                         this.$axios.defaults.headers.common['Authorization'] = "Token " + localStorage.getItem('auth_token'))))
      .catch(error => {this.info = error.response;
                       let data = error.response.data;
                       this.non_field_errors = data.non_field_errors ? data.non_field_errors.join(' ') : null;
                       this.username_errors = data.username ? data.username.join(' ') : null;
                       this.password_errors = data.password ? data.password.join(' ') : null; });
    }
  }
}
</script>

<style scoped>
form {
  margin-top: 7%;
  display: flex;
  flex-direction: column;
}
</style>