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
                    v-for="(item, index_j) in row" :key="item" @click="click_on_item(item, index_i, index_j)">
                        <div :class="{crosspos: item.readypos && item.blueitem,
                                    circlepos: item.readypos && item.reditem, 
                                    squarepos: item.readypos && item.greenitem, 
                                    diamondpos: item.readypos && item.purpitem, 
                                    firstpos: item.firstpos, 
                                    purpitem: item.purpitem && item.firstpos, 
                                    reditem: item.reditem && item.firstpos, 
                                    blueitem: item.blueitem, 
                                    greenitem: item.greenitem && item.firstpos}" > 

                                 <!-- {{item.w}}{{item.h }} {{index_i}}  -->
                        </div>
                        
                    </div>
                </div>
            </div>
            <div class="info-game">
                {{game_message}}
            </div> 
            <div class="info-game">
                <span v-html="winer"></span> 
            </div> 
            <button class="give-up" v-if="game_state==2" @click="refresh_field">
                ОK
            </button>
            <button class="give-up" v-if="game_state==1" @click="give_up">
                Сдаться
            </button>
        
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
                Игроки:
                <div class="player" v-for="m in players" :key="m.name" :class="{purptxt: m.purpitem, redtxt: m.reditem, bluetxt: m.blueitem, greentxt: m.greenitem}">
                     {{ m.index + " " + m.name }}
                </div>

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
      message: "",
      battlefield: [],
      hist_messages: [],
      players: [],
      chat_socket: WebSocket, 
      game_state: 0, 
      game_message: "Выберите позицию", 
      cur_figure: null,
      username: null, 
      winer: ""
      }
    },
    methods : {
        GotoLobby() {
            this.$router.push({name: "lobby"});
        },
        SendMSG() {
            if (!(this.message === ""))
            {
                this.chat_socket.send(JSON.stringify({
                    'type': 'chat',
                    'content': this.message
                }));
                this.message = '';
            }
        },
        refresh_field(){
             //location.reload()
            this.game_state = 0;

            this.winer = "";
            this.create_board();
            this.websocket_connection(); //location.reload()
        },
        give_up() {
            //this.create_board();
            //this.websocket_connection();
            //location.reload()
            
            this.chat_socket.send(JSON.stringify({
                    'type': 'remove_player'
                }));
        },
        readiness(item, i, j){
            if (item.firstpos || item.readypos){
                let figure = 0
                
                if (i === 0 && j === 0) figure = 1;
                else if (i === 0 && j === this.room.width-1) figure = 2;
                else if (i === this.room.height-1 && j === 0) figure = 3;

                else figure = 4          

                this.chat_socket.send(JSON.stringify({
                    'type': 'readiness',
                    'figure': figure
                }));
            }
        },
        game_over() {
            this.game_message = "Конец битвы!"
            this.game_state = 2;
            this.info += this.game_state;
            if (this.cur_figure != null){
                for (let m in this.players)
                    if (this.players[m].numb == this.cur_figure)
                        this.winer = "Победил вирус " + this.players[m].name + "!";
            }
            else this.winer = "Победила Ничья!";          
        },
        take_move(item, i, j) {
            //if (this.username === )
            this.info = i + j;
            for (let m in this.players)
            {
                if (this.username === this.players[m]["name"] && this.players[m]["numb"] == this.cur_figure){
                    this.chat_socket.send(JSON.stringify({
                    'type': 'take_move',
                    'i': i,
                    'j': j
                    }));
                }
            }
        },
        draw_move(cell, i, j){
            //this.info += "cell - "+ cell + " "+ i+ j;
            this.battlefield[i][j].firstpos = false;
            
            if (cell < 10){
                 this.battlefield[i][j].readypos = true;
                if (cell ==  1) this.battlefield[i][j].blueitem = true;
                else if (cell ==  3) this.battlefield[i][j].purpitem = true;
                else if (cell ==  2) this.battlefield[i][j].greenitem = true;
                else if (cell ==  4) this.battlefield[i][j].reditem = true;
            }
            else {
                let div = parseInt(cell/10)
                
                let mod = cell % 10; // 12 - второ й побил 1 
                if (div ==  1) this.battlefield[i][j].blueitem = true, this.battlefield[i][j].readypos = true;
                else if (div ==  3) this.battlefield[i][j].purpitem = true, this.battlefield[i][j].readypos = true;
                else if (div ==  2) this.battlefield[i][j].greenitem = true, this.battlefield[i][j].readypos = true;
                else if (div ==  4) this.battlefield[i][j].reditem = true, this.battlefield[i][j].readypos = true;

                if (mod ==  1) this.battlefield[i][j].bluebg = true;
                else if (mod ==  3) this.battlefield[i][j].purpbg = true;
                else if (mod ==  2) this.battlefield[i][j].greenbg = true;
                else if (mod ==  4) this.battlefield[i][j].redbg = true;
            }
            
        },
        click_on_item(item, i, j) {
            this.info += "click" + this.game_state;
            if (this.game_state === 0) // игруля не началась // это обработка занять позиции
            {
                this.readiness(item, i, j);
            }
            else if (this.game_state === 1)
            {
                this.take_move(item, i, j);
            }
        },
        paint_board(board) {
            if (board == null)
                this.create_board()
            

            for (let i in board) {
                for (let j in board) {
                    this.draw_move(board[i][j], i, j)
                }
            }
        },
        print_blocked(ready_players, code) {
            //this.winer = "";
            for (let m in this.players)  {
                
                //if (this.players[m].name == this.username){
                
                let exist = false;
                for (let cur in ready_players)
                
                    if (this.players[m].numb == ready_players[cur]){
                        exist = true;
                        break;
                    }
                
                if (!exist) {
                    
                    if (code != 3) this.winer += "Вирус " + this.players[m].name + " завершает свое существование! <br>";
                    if (this.players[m].name == this.username && this.cur_figure != this.players[m].numb) alert("Вы проиграли!"), this.game_state = 2; 
                }

            }
            this.paintready(ready_players)

        },
        paintready(ready_players){
            this.info += "paint ready ||" + this.game_state + "||";
            if (this.game_state == 0)
                for (let m in this.players) {
                    if (this.players[m]["numb"] === 1) 
                        this.battlefield[0][0].readypos = false,
                        this.battlefield[0][0].firstpos = true;

                    if (this.players[m]["numb"] === 3) 
                        this.battlefield[this.room.height-1][0].readypos = false,
                        this.battlefield[this.room.height-1][0].firstpos = true;
                    if (this.players[m]["numb"] === 2) 
                        this.battlefield[0][this.room.width-1].readypos = false,
                        this.battlefield[0][this.room.width-1].firstpos = true;
                    if (this.players[m]["numb"] === 4) 
                        this.battlefield[this.room.height-1][this.room.width-1].readypos = false,
                        this.battlefield[this.room.height-1][this.room.width-1].firstpos = true;
                }

            this.players = [];
            let ind = 1;
            for (let m in ready_players){
                //this.info += m + "haha",
                this.players.push({ name: m, numb: ready_players[m], index: ind});
                ind +=1;
            }

            //this.info += this.players;
            for (let m in this.players) {
                //this.info += this.players[m].numb + "!" + this.players[m].numb == 2 ;
                if (this.players[m]["numb"] == 1) {
                    this.players[m].blueitem = true,
                    this.battlefield[0][0].firstpos = false;
                    this.battlefield[0][0].readypos = true;
                    this.battlefield[0][0].blueitem = true;
                    this.info += this.battlefield[0][0].blueitem + this.battlefield[0][0].readypos + this.battlefield[0][0].firstpos;
                }
                if (this.players[m]["numb"] == 3) {
                    this.players[m].purpitem = true;
                    this.battlefield[this.room.height-1][0].purpitem = true;
                    this.battlefield[this.room.height-1][0].firstpos = false;
                    this.battlefield[this.room.height-1][0].readypos = true;
                }
                if (this.players[m]["numb"] == 2) {
                    this.players[m].greenitem = true; 
                    this.battlefield[0][this.room.width-1].greenitem = true;
                    this.battlefield[0][this.room.width-1].firstpos = false;
                    this.battlefield[0][this.room.width-1].readypos = true;
                }
                if (this.players[m]["numb"] == 4) {
                    this.players[m].reditem = true, 
                    this.battlefield[this.room.height-1][this.room.width-1].reditem = true;
                    this.battlefield[this.room.height-1][this.room.width-1].firstpos = false;
                    this.battlefield[this.room.height-1][this.room.width-1].readypos = true;
                }
            }
            
        },
        start() {
            this.chat_socket.send(JSON.stringify({
                    'type': 'start'
                }));
        },
        check_datacode(code){
            let cur_user = '';
            for (let m in this.players) 
                {if (this.players[m].numb == this.cur_figure) cur_user = this.players[m].name;}

            if (code == 0) this.game_message = "Ход игрока " + cur_user;
            if (code == 3) this.game_over();
            if (code == 1) this.game_message = "Игра не идет";
        }, 
        websocket_connection() {
          this.chat_socket = new WebSocket(this.$ws + '/room/' + this.$route.params.id + '/' );
          
          this.chat_socket.onopen = e =>  {
            this.info += "ws подключено" + e;
            let auth_data = {  'type': 'auth',
                                'token': localStorage.getItem('auth_token') }
            this.chat_socket.send(JSON.stringify(auth_data));

            this.$axios.get('/api/messages-room/' + this.$route.params.id )
            .then(response => {
                this.hist_messages = response.data;
            })
            .catch()
          };
          
          this.chat_socket.onclose = eventclose => {
            this.info += 'соеденение закрыто причина: ' + eventclose
          };
          this.chat_socket.onmessage = msg => {
            this.info += 'Сообщение ' + msg.data ;
           
            let data = JSON.parse(msg.data);

            if (data.type === "chat")
            {
                this.hist_messages.unshift({'user': data.user,'datetime': data.datetime,  'content': data.content});
            }

            else if (data.type === "readiness")
            {
                this.paintready(data.ready_players)
            }
            else if (data.type === "start"){
                let code = data.code
                if (code == 0)
                {
                    this.cur_figure = data.cur_figure;
                    this.game_state = 1;
                    this.info += "start" + this.game_state;
                    let cur_user = '';
                    for (let m in this.players) 
                        {if (this.players[m].numb == this.cur_figure) cur_user = this.players[m].name;}
                    this.game_message = "Игра началась! Ход игрока " + cur_user;
                }
            }
            else if (data.type === "connect"){
            
                if (data.code === 1)
                {
                    this.paintready(data.ready_players);
                    this.game_message = "Выберите позицию";
                    if (!data.ready_players) this.paint_board(data.board);
                }
                else if( data.code == 0){
                    this.paintready(data.ready_players);
                    this.paint_board(data.board)
                    //this.info += "going"
                    this.game_message = "Игра идет";
                }

            }
            else if (data.type === "take_move")
            {
                //let code = date.code; // конец игры - 0 не идетт - 1  конец игры - 3
                let is_implemented = data.is_implemented;
                this.cur_figure = data.cur_figure;
                
                this.check_datacode(data.code); 

                this.print_blocked(data.ready_players,  data.code);
                
                if (is_implemented) this.draw_move(data.cell, data.i, data.j);
                  
            }
            else if(data.type === "remove_player"){
                this.cur_figure = data.cur_figure;
                this.check_datacode(data.code); 
                this.print_blocked(data.ready_players,  data.code);
                this.paintready(data.ready_players);
                
            }
            else if (data.type === "readiness_personal")
            {      
                switch ( data.code) {
                    case 0:
                        this.game_message = "Игра идет";
                        break;
                    case 2:
                        this.game_message = "Сейчас игра начнется";
                        this.start()
                        break;
                    case 1:
                        this.game_message = "Ожидание игроков";
                        break;
                    case 3:
                        this.game_message = "Игра закончилась";
                        break;
                    case 4:
                        this.game_message = "Ожидание игроков, позизия выбрана";
                        break;    
                    case 5:
                        this.game_message = "Ожидание игроков, вы отменили готовность";
                        break;
                    case 6:
                        this.game_message = "Ожидание игроков, позиция изменена";
                        break;
                    case 7:
                        this.game_message = "Ожидание игроков, позиция занята другим игроком";
                        break;
                    case 8: 
                        this.game_message = "Готовых игроков нет, выберите позицию"; 
                        break;
                }
            }
          };
        },
        create_board() {
            this.battlefield = [];
            for (let n = 0; n < this.room.height; n++) {
            this.battlefield.push([]);
            for (let m = 0; m < this.room.width; m++){
                this.battlefield[n].push(
                    {}
                    );
                
                if (n == 0 && m == 0) this.battlefield[n][m].firstpos = true, this.battlefield[n][m].blueitem = true;
                if (n == this.room.height-1 && m == this.room.width-1) this.battlefield[n][m].firstpos = true, this.battlefield[n][m].reditem = true;

                if (this.room.max_players == 4){
                    if (n == this.room.height-1 && m == 0) this.battlefield[n][m].firstpos = true, this.battlefield[n][m].purpitem = true;
                    if (n == 0 && m == this.room.width-1) this.battlefield[n][m].firstpos = true, this.battlefield[n][m].greenitem = true;
                }
                    
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
          
          this.websocket_connection();
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
    destroyed(){
        this.chat_socket.close();
    }    
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
#info-game {
    font-size: 120%;
    margin: 1vh;
    width: 100%;
}
.give-up {
  border:paleturquoise;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  font-family: Comic Sans MS, Comic Sans, cursive;
  margin: 1vh;
  color: white;
  font-size: 100%;
}
.give-up:hover {
    background: rgb(29, 175, 211);
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
.msg-user{
    color: Navy;
    margin: 0 1% 0 0;
}
.msg-datetime {
    color: Gainsboro;
    font-size: 80%;
    margin: auto 0;
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
#players {
    text-align: left;
    margin: 1vh;
}
.player {
    border-radius: 100px 100px 100px 100px;
    background: white;
    width: 30%;
    min-width: 200px;
    padding: 0.1vh;
    padding-left: 2vh;
    margin: 0.5vh 0 0.5vh 0;
    text-align: left;
    
}
.firstpos {
    margin-left: 0.5vh;
    margin-top: 0.5vh;
    background: grey;
    height: var(--item-size);  
    width: 0.3vh; 
    position: relative; 
    left: 1.35vh; 
}
.firstpos:after {
    content: "";
    height: 0.3vh; 
    width: var(--item-size);
    background: grey;
    position: absolute; 
    left: -1.35vh; 
    top: 1.35vh;
}

.crosspos {
    margin-left: 0.5vh;
    margin-top: 0.5vh;
    background: grey;
    height: var(--item-size);  
    width: 0.2vh; 
    position: relative; 
    left: 1.35vh; 
    
}

.crosspos:after{
    content: "";
    height: 0.2vh; 
    width: var(--item-size);
    background: grey;
    position: absolute; 
    left: -1.35vh; 
    top: 1.35vh;
    
}
.crosspos {
    transform: rotate(45deg);
}

.circlepos {
    margin-left: 0.8vh;
    margin-top: 0.8vh;
	width: 2vh;
	height: 2vh;
    
    background: transparent;
    border: 0.2vh solid red;
	border-radius: 50%;
	/*border-radius: 1.5vh;*/
}

.squarepos {
    margin-left: 0.8vh;
    margin-top: 0.8vh;
	width: 2vh;
	height: 2vh;
	background: transparent;
    border: 0.2vh solid rgb(10, 151, 10); 
}

.diamondpos {
    margin-left: 1.95vh;
    margin-top: 1.5vh;
    width: 1.5vh;
    height: 1.5vh;
    background: transparent;
    border: 0.2vh solid rgb(53, 50, 50);
/* Rotate */
    -webkit-transform: rotate(-45deg);
    -moz-transform: rotate(-45deg);
    -ms-transform: rotate(-45deg);
    -o-transform: rotate(-45deg);
    transform: rotate(-45deg);
/* Rotate Origin */
    -webkit-transform-origin: 0 100%;
    -moz-transform-origin: 0 100%;
    -ms-transform-origin: 0 100%;
    -o-transform-origin: 0 100%;
    transform-origin: 0 100%;
    
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
.grey {
    background: rgb(219, 218, 218);
}
.purpitem, .purpitem:after {
    background: rgb(53, 50, 50);
}
.greenitem, .greenitem:after{
    background: rgb(10, 151, 10);
}
.blueitem, .blueitem:after{
    background: rgb(50, 50, 255);
}
.reditem, .reditem:after{
    background: rgb(255, 50, 50);
}
.purptxt {
    color: rgb(53, 50, 50);
}
.greentxt{
    color: rgb(10, 151, 10);
}
.bluetxt{
    color: rgb(50, 50, 255);
}
.redtxt{
    color: rgb(255, 50, 50);
}
</style>
