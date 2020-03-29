<template>
  <div id="page-lobby">
    <div id="tool-bar" >

    <div class="btns">
      <button class='btn-room' @click="ShowModal()">
        <p id="create-text">Создать <br />комнату</p>
        <img id="pen" src="../../assets/images/pen.png" height="40px"/>
      </button>
      <button class='btn-room' >
        <p v-if="searchroom_form.starred"> Все<br /> комнаты</p>
        <p v-else> Избранные<br /> комнаты</p>
      </button>
    </div>

    <!-- 
    <div class="checkboxes">
      <label class="big_chk">
          <input type="checkbox" id="empty" />
          <span></span>
          <div class="check-descrpt">Скрыть пустые комнаты </div>
      </label>
      <label class="big_chk">
          <input type="checkbox" id="filled" />
          <span></span>
          <div class="check-descrpt"> Скрыть занятые комнаты </div>
      </label>
    </div>
    -->
  
    <div class="search-block searches">
      <input id="search-text" v-model="searchroom_form.search" > Поиск
    </div>
    <modal-create-room v-show="isModalCreateVisible" @close="closeModal"/> 
  </div>
    
    <div id="rooms-list"> 
      <div class="contain-row">
        <div id="head-table" class="item">
          <div class="access">Доступ </div>
          <div class="name">Название</div>
          <div class="players">Игроки </div>
          <div class="size">Размер </div>
        </div>
      </div>

      <div class="contain-row" v-for="room in rooms" :key="room.id">
        <div class="item" >
          <div class="access" v-if='room.password'> <img id="pen" src="../../assets/images/zamok.png" height="20px" /> </div>
          <div class="access" v-else>  </div>
          <div class="name"> {{room.name}} </div>
          <div class="players"  :class="{busy: room.is_on}" > {{room.players}}/{{room.max_players}} </div>
          <div class="size"> {{room.height}}x{{room.width}} </div>
        </div>
        <button class="starred" >
          <div class="star" v-if="room.is_starred" > ★ </div>
          <div class="star" v-else >  ☆ </div>
        </button>
      </div>
    </div>
    <div v-show="false">
      {{info}} 
    </div>
  </div>
</template>

<script>
import ModalCreateRoom from './ModalCreateRoom.vue';

export default {
  name: "PageLobby",
  components:{
    ModalCreateRoom,
  },
  data () {
    return {
      rooms : [], 
      info: null, 
      isModalCreateVisible: false,
      searchroom_form: {
        hide_empty: false,
        hide_busy: false, 
        starred: false,
        search: "",
      },
      destinationroom: null
    }
  },
  methods: {
    ShowModal() { this.isModalCreateVisible = true; },
    closeModal() { this.isModalCreateVisible = false;  }, 
    
  }, 

}
</script>


<style scoped>
#rooms-list {
  text-align: left;
}
#head-table {
  background-color: transparent;
}
.item {
  background-color: rgba(20, 0, 255, 0.2);
  border-radius: 200px 0px;
  padding: 8px 0;
  width: 96%;
  cursor: pointer;
  display: flex;
  flex-direction: row;
}
.item:hover {
  background: RoyalBlue;
}
.contain-row{
  display: flex;
  flex-direction: row;
  width:65%;
  margin: 5px auto;
  
}
.busy {
  color: SpringGreen;
}
.access {
  margin-left: 3%;
  width: 16%;
}
.name, .players, .size {
  width: 28%;
}
.starred{
  margin: auto;
  background: transparent;
  color: white;
  cursor: pointer;
  outline: none;
  border: none;
}
@media (max-width: 800px) {
  .contain-row {
    width:90%;
    font-size: 90%;
  }
}
.star {
  font-size: 150%;
}
.star:hover {
  font-size: 200%;
}
.searches{
  cursor: pointer;
}
#tool-bar {
  background-color: rgba(242, 242, 242, 0.3);
  border-radius:  150px;
  width:45%;
  min-width: 650px;
  height: 10%;
  margin: 30px auto 5px auto;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.checkboxes {
  display: flex;
  flex-direction: column;
  margin-top: 5px;
  width: 30%;
}
.btns {
  display: flex;
  flex-direction: row;
  width: 45%;
}
.btn-room {
  background-color: rgba(45, 156, 219, 0.5);
  border-radius:  150px;
  margin: 5px 5px;
  padding: 3px;
  font-size: 83%;
  width: 50%;
  display: flex;
  flex-direction: row;
  font-family: Comic Sans MS, Comic Sans, cursive;
  color: white;
  outline: none;
  border: none;
}
.btn-room:hover {
  background-color: SteelBlue;
}
#pen{
  margin-right: 10px;
  margin-bottom: -2px;
}
#create-text{
  margin-right: -10px;
}
img, p { 
  margin: auto;
}
.big_chk {
  cursor: pointer;
  margin: 0 auto 0 0;
  font-size: 90%;
  display: flex;
  flex-direction: row;
}
.big_chk input {
  padding: 0px;
  margin-right:-16px;
  visibility: hidden;
}
.big_chk input + span {
  display: inline-block;
  width: 25px;
  height: 25px;
  background: url('../../assets/images/sprite.png') left/210%  no-repeat;
}
.big_chk input:checked+span {
  background-position: right ;
}

.check-descrpt{
  margin-left:1vh;
}
.search-block{
  width: 55%;
  margin: auto 0;
  font-size: 90%;
}
#search-text {
  background-color: white;
  text-align: center;
  border: 0px;
  border-radius: 100px 100px 0px 100px;
  font-family: Comic Sans MS, Comic Sans, cursive;
  font-size: 90%;
  width: 60%;
  outline: none;
}

@media (max-width: 650px) {
  #tool-bar {
    display: flex;
    flex-direction: column;
    width: 90%;
    min-width: auto;
    border-radius:  30px;
  }

  .checkboxes, .btns, .search-block, .big_chk {
    width: 100%;
    margin-left: 10px;
    justify-content: center;
    margin: auto 0;
    margin-bottom: 1vh;
  }
}
</style>