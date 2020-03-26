<template>
  <div id="page-lobby">
    <div id="tool-bar" >

    <div class="btns">
      <button class='btn-room' >
        <p id="create-text">Создать <br />комнату</p>
        <img id="pen" src="../../assets/images/pen.png" height="40px"/>
      </button>
      <button class='btn-room' >
        <p v-if="searchroom_form.starred"> Все<br /> комнаты</p>
        <p v-else> Избранные<br /> комнаты</p>
      </button>
    </div>
  
    <div class="search-block searches">
      <input id="search-text" v-model="searchroom_form.search"> Поиск
    </div>
    <modal-create-room /> 
    <modal-get-room-password :room="destinationroom" /> 
  </div>

    <div v-show="false">
      {{info}} 
    </div>
  </div>
</template>

<script>

export default {
  name: "PageLobby",
  data () {
    return {      
      info: null, 
      searchroom_form: {
        starred: false,
        search: "",
      },
    }
  },
  
}
</script>


<style scoped>

#head-table {
  background-color: transparent;
}
.contain-row{
  display: flex;
  flex-direction: row;
  width:65%;
  margin: 5px auto;
  
}

@media (max-width: 800px) {
  .contain-row {
    width:90%;
    font-size: 90%;
  }
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

   .btns, .search-block {
    width: 100%;
    margin-left: 10px;
    justify-content: center;
    margin: auto 0;
    margin-bottom: 1vh;
  }
}
</style>