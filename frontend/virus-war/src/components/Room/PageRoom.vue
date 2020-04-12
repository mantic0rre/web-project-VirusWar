<template>
<div id="page-room">      
    
    <div class="stat-line">
        <div class="stat-line-contain">
            <div class="stat-text">{{ room.name }} </div>
            <div id="go-lobby" v-on:click="GotoLobby()"> 
                <div class="stat-text"> Выйти  в лобби </div>
                <img id="door-icon" src="../../assets/images/DoorIcon.png" height="30px"/> 
            </div>
        </div>
    </div> 
    
    
    <div class="game-content">
        <div class="game">
            <div class="field-size">
            {{room.height}} x {{room.width}} 
            </div>
            <div id="battlefield">
                <div class="field-row" v-for="(row, index_i) in battlefield" :key="row">
                    <div class="field-item" 
                    :class="{grey: item.firstpos && !item.readypos,  purpitem: item.purpbg, reditem: item.redbg, blueitem: item.bluebg, greenitem: item.greenbg}" 
                    v-for="item in row" :key="item" >
                        {{item.w}}{{item.h }} {{index_i}}  
                    </div>
                </div>
            </div>
            <div class="info-game">
                {{game_message}}
            </div> 
            
        
        </div>
        
        <div class="game-info">
            <div class="field-size">
            
            </div>
            <div id="chat">
                <form class="chat-form" @submit.prevent="SendMSG()">
                    <input v-model="message"/>
                    <button id="send-btn"> Отправить </button>
                </form>
                <div id="msg-area">
                    <div class="msg" v-for="m in hist_messages" :key="m.id">
                    <div class="msg-prop"> 
                        <div class="msg-user"> {{m.user}} </div> 
                        <div class="msg-datetime"> {{m.datetime}} </div> 
                    </div>
                    <div class="msg-content"> {{m.content}} </div>
                    </div>
                </div>
            </div>
            <div id="players">
                Игроки
                

            </div>

        </div>
    </div>
    <!-- {{info}} -->
</div>
</template>

<script>


export default {
    name: "PageRoom",
    data () {
    return {
      room : {},// {name: null, length: null, width: null }, 
      info: null, 
      battlefield: [],
      chat_socket: WebSocket, 
      game_message: "Выберите позицию", 
      username: null, 
      hist_messages: [],
      }
    },
    methods : {
        GotoLobby() {
            this.$router.push({name: "lobby"});
        },
        
        create_board() {
            this.battlefield = [];
            for (let n = 0; n < this.room.height; n++) {
            this.battlefield.push([]);
            for (let m = 0; m < this.room.width; m++){
                this.battlefield[n].push(
                    {}
                    );
                
                    
              }
          } 
        }
    },
    beforeCreate() 
    {
      
      this.$axios.get('/api/rooms/' + this.$route.params.id )
      .then(response => 
      {
          this.info += response.data;
          this.room = response.data;

          this.create_board();
          
        
      })
      .catch(error => { 
          if(error.response.status == 401) 
            this.$router.push({name: "root"});
      });

      this.$axios.get('/api/auth/users/me/')
      .then(response => ( this.username = response.data.username) )
      .catch(error => { 
          if(error.response.status == 401) 
            this.$router.push({name: "root"});
      });
    },
}
</script>

<style scoped>
.stat-line{
    margin-top: 2vh;
    background: rgba(242, 242, 242, 0.3);

}
.stat-line-contain{
    display: flex;
    flex-direction: row;
    font-size: 90%;
    justify-content: space-around;
    max-width: 1400px;
    margin: auto;
}
.stat-text{
    margin: auto 0;
    font-size: 120%;
}
#go-lobby {
    display: flex;
    flex-direction: row;
    cursor: pointer;
}
.game-content{
    
    margin: 0vh auto 0 auto;
    display: flex;
    flex-direction: row;
    justify-content: center;
    max-width: 1500px;
}
.field-size{
    font-size: 130%;
    height: 6vh;
    margin-bottom: 0.5vh;
    color: transparent;
    -webkit-text-stroke-width: 0.5px;
    -webkit-text-stroke-color: white;
}
.field-row{
    display: flex;
    flex-direction: row;
    margin-right: 0;
    justify-content: center; /* flex-end;*/
}
#battlefield {
    margin-right: 0;
}
.field-item{
    width: 4vh;
    height: 4vh;
    color: black; 
    background: white;
    border: 0.3px solid rgba(47, 128, 237, 0.3);
    --item-size: 3vh;
}
.field-item:hover{ 
    border: 0.3px double blue;
}
.game, .game-info{
margin: 2vh 5vh;

}
.game {
    justify-content: right;
}
.game-info{
    width: 40%;
} 


#chat{
    width: 100%;
    height: 40vh;
    background: rgba(0, 193, 255, 0.1);
    border: 0.7px solid #FFFFFF;
    box-sizing: border-box;
    border-radius: 20px;
    display: flex;
    flex-direction: column-reverse;
}

#players {
    text-align: left;
    margin: 1vh;
}

.chat-form{
    align-items: flex-end;
}
input{
  background-color: white;
  border: 0px;
  border-radius: 100px 100px 0px 100px;
  margin: 0% 0% 2% 0;
  padding: 0% 2%;
  font-family: Comic Sans MS, Comic Sans, cursive;
  width: 80%;
  min-width: 100px;
  height:35px;
  outline: none;
}
#send-btn{
    background-color: transparent;
    border: none;
    cursor: pointer;
    outline: none;
}
#msg-area{
    overflow-y: scroll;
    display: flex;
    flex-direction: column-reverse;
    margin-left: 2%;
    font-size: 90%;
}
.msg-prop {
    text-align: left;
    
    display: flex;
    flex-direction: row;
}
.msg-content {
    text-align: left;
    background-color: transparent;
    margin-bottom: 2%;
    
}
.msg-content, .msg-prop
{
    border-radius: 100px 100px 100px 100px;
}
.msg-user{
    color: Navy;
    margin: 0 1% 0 0;
}
.msg-datetime {
    color: Gainsboro;
    font-size: 80%;
    margin: auto 0;
}

@media (max-width: 650px) {
    
    .game-content{
        margin: 1vh auto 0 auto;
        display: flex;
        flex-direction: column;
    }
    .field-row {
        margin: 0 1vh 0 1vh;
    }
    
    .game-info{
        width: 90%;
        margin: 2vh auto 2vh auto;
    } 
    
}

</style>

