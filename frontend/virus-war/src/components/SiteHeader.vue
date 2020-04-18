<template>
<div id="header">
  <header>
    <div id='logo'> Virus War </div>
    <div id="persona"> 
      <div id='user' >  {{username}} <button v-if="logout" @click="log_out" id="log-out"> Выйти </button> </div>
      <div id='btnblock'> <button id='howplay' type="button" @click="$emit('modalShow')"> Как играть? </button> </div>
    </div>
  </header>
</div>
</template>

<script>
export default {
  name: 'SiteHeader',
  props: ['user'], 
  data () {
    return { 
      username: ' ',
      logout: true
    }
  },
  methods: {
    log_out(){
      this.$router.push({name: "root"});
    }
  },
  watch: {
    user: function () {
      this.username = this.user;
      if (this.user == null) this.logout= false;
      else this.logout=true;
    }
  },
  created() {
    let elem = document.getElementById('start-page');
    if (!elem) {
      this.$axios.get('/api/auth/users/me/')
        .then(response => ( this.username = response.data.username) )
        .catch(error => {this.username = " ", this.info = error})
    }
  }
}
</script>

<style scoped>
#header {
  background: rgba(242, 242, 242, 0.3);
}
header {
  display: flex;
  flex-direction: row;
  max-width: 1500px;
}
#logo {
  flex: 2;
  font-family: Pecita;
  font-size: 280%;
  margin: auto 0;
  color: transparent;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: white;
}
#persona {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding-right: 10%;
  text-align: center;
}
#log-out {
  cursor: pointer;
  outline: none;
  background: transparent;
  border: white;
  color: white;

}
#log-out:hover {
  background: RoyalBlue;
}
#user {
  display: flex;
  justify-content: center;
  height: 3vh;
  margin-top: 0.5em;
}

#btnblock {
  flex: 1;
  font-size: 75%;
  margin: 0.5em 0;
  padding-right: 10%;
}
#howplay {
  border:paleturquoise;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  font-family: Comic Sans MS, Comic Sans, cursive;
  color: white;
  font-size: 100%;
}
#howplay:hover {
    background: rgb(61, 99, 224);
}
@media (max-width: 650px) {
  #logo {
    font-size: 1.7em;
    flex: 1;
  }
  #persona {
    padding-right: 3%;
    flex: 1;
  }
  #username {
    font-size: 75%;
  }
}
</style>