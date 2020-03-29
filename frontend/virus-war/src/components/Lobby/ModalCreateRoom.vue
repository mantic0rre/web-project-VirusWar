
<template>
  <div class="modal-backdrop">
    <div class="modal">
      <header class="modal-header">
        
          <div class="header-text"> Создать комнату
          </div>
          
              <button
            type="button"
            class="btn-close"
            @click="close"
          >
            x
            </button>
          
          
      </header>
      <section class="modal-body">
        <slot name="body">
          
            <form id="form-create-room" >
                <div class="form-text"> Название комнаты: </div>
                <base-input type="text" name="name"/>
                <div class="auth-error"> {{ roomname_errors }} </div> 

                <div class="form-text"> Максимальное количество игроков: </div>
                <input type="radio" name="max_players" value="2">
                <label >2</label> 
                <input type="radio" name="max_players" value="4">
                <label >4</label>
                
                <div class="auth-error"> {{ maxplayers_errors }} </div> 

                <div class="form-text"> Размер поля: </div>
                <input type="radio" name="size" value="10 x 10">
                <label >10 x 10</label> 

                <input type="radio" name="size" value="10 x 15">
                <label >10 x 15</label> 

                <input type="radio" name="size" value="15 x 15">
                <label >15 x 15</label> 
                
                <div class="auth-error"> {{ length_errors }} {{ width_errors }} </div> 
                <div class="form-text"> Пароль:  </div>
                <base-input type="password" name="password" />
                <div class="auth-error"> {{ password_errors }} </div> 

                <div class="auth-error"> {{ non_field_errors }} </div>
                <button class="auth-button"> Создать </button>
            </form>   
            
        </slot>
       </section>
      
    </div>

  </div>
</template>
<script>
import BaseInput from '../BaseInput.vue'

  export default {
    name: 'modal',
    components: {
        BaseInput
    },
    data() {
        return {
            selected: "",
            form_data: "",
            info: "", 
            non_field_errors: "", 
            password_errors: "", 
            width_errors: "", 
            length_errors: "",
            maxplayers_errors: "", 
            roomname_errors: ""
        }
    },
    methods: {
      close() {
        this.$emit('close');
      },
      
    }
  };
</script>

<style >
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
  width: 50%;
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
</style>