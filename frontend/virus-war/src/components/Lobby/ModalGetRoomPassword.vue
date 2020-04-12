<template>

    <div class="modal-backdrop">
      <div class="modal"
           role="dialog"
           aria-labelledby="modalTitle"
           aria-describedby="modalDescription"
      >
        <div id="modalTitle" class="modal-header head-text">
          <div class="head-text"> Комната {{destinationRoom.name}}</div> 
          <button type="button"
                  class="btn-close"
                  @click="closePC"
                  aria-label="Close modal"
          >
            x
          </button>
        </div>

       <section class="modal-body">
        <slot name="body">
          
            <form id="form-validate" @submit.prevent="validatePassw()">
                
                <div class="form-text"> Пароль:  </div>
                <base-input id="passw" type="password" name="password"/>
                <div class="auth-error"> {{ password_error }} </div> 
                <button class="auth-button"> Войти </button>
            </form>        
        </slot>
       </section>
      </div>
    </div>

</template>

<script>
import BaseInput from '../BaseInput.vue'

  export default {
    name: 'ModalGetRoomPassword',
    props: ['room'], 
    components: {
        BaseInput
    },
    data () {
      return { 
      destinationRoom: {}, 
      info: "ar", 
      iscorrrect: false,
      password_error: ""
      }
    },
    methods: {
      validatePassw(){
        let val = document.getElementById("passw");
        //this.info = val.value;
        if (val.value === this.destinationRoom.password)
          this.$emit('closePasswordCheck', true);
        this.password_error = "Неправильный пароль";
      }, 
      closePC() {
        this.$emit('closePasswordCheck', this.iscorrrect);
      }
    },
    watch: {
    room: function () {
      this.destinationRoom = this.room;
      this.info = this.room;
    }
  }
  };
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: #3C73C5;
  box-shadow: 2px 2px 20px 1px;
  margin-top: 5vh;
  display: flex;
  width: 30%;
  flex-direction: column;
  max-width: 1000px;
}

.modal-header {
  padding: 15px;
  display: flex;
  flex-direction: row;
  color: white;
  width: 95%;
  justify-content: space-between;
}
.header-text {
  margin-left: 5%;
  width: 90%;
}
.modal-body {
  position: relative;
  padding: 20px 10px;
}

.btn-close {
  border: none;
  font-size: 20px;
  padding: auto;
  cursor: pointer;
  font-weight: bold;
  color: white;
  background: transparent;
  
}
.form-text {
  margin-top: 1%;
}

label {
  margin: 2% 5% 0 0;
}

@media (max-width: 650px) { 

  .modal {
    width: 70%;
  }
}
</style>