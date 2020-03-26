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
    registered() {
      this.is_registered = true;
      this.username = '';
      this.password = '';
      this.password_repeat = '';
    },
    clearErrors() {
      this.password_repeat_err = '';
      this.non_field_errors = '';
      this.username_errors = '';
      this.password_errors = '';
    },
    signUp() { 
      this.is_registered = false;
      this.clearErrors();

      if (this.password === this.password_repeat) {
        let form = document.getElementById("form-register");
        let form_data = new FormData(form);

        // для отображения ошибки с пустым полем
        for(let pair of form_data.entries()) {
          pair[1] ? null: form_data.set([pair[0]], ' ');
        }

         this.$axios.post('/api/auth/users/', form_data)
         .then(response => { this.registered(); 
                             this.info = response.status; })
         .catch(error => {let data = error.response.data;
                          this.non_field_errors = data.non_field_errors ? data.non_field_errors.join(' ') : null;
                          this.username_errors = data.username ? data.username.join(' ') : null;
                          this.password_errors = data.password ? data.password.join(' ') : null; });
      }
      else
        this.password_repeat_err = this.password_repeat ? 'Пароли не совпадают.' : 'Подтвердите пароль.';
    },
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