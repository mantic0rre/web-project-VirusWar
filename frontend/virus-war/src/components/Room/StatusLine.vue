<template>
    
        <div id="status-line" class="stat-line">
            <div class="stat-line-contain">
                <div class="stat-text">{{ room.name }} </div>
                <div id="go-lobby" v-on:click="GotoLobby()"> 
                    <div class="stat-text"> Выйти  в лобби </div>
                    <img id="door-icon" src="../../assets/images/DoorIcon.png" height="30px"/> 
                </div>
            </div>
        </div>
    
    
</template>

<script>
export default {
    name: 'StatusLine', 
    methods: {
        GotoLobby() {
            this.$router.push({name: "lobby"});
        }
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

</style>