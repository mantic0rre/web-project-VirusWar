<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div class="modal"
           role="dialog"
           aria-labelledby="modalTitle"
           aria-describedby="modalDescription"
      >
        <div id="modalTitle" class="modal-header head-text">
          <div class="head-text"> Как играть? </div> 
          <button type="button"
                  class="btn-close"
                  @click="$emit('close')"
                  aria-label="Close modal"
          >
            x
          </button>
        </div>

        <section id="modalDescription" class="modal-body">
          <slot name="body">
            <div class="stage"> Начало </div>
            <div class="rulestext">
              Игра проходит на прямоугольном клетчатом поле (в официальных турнирах 10 см на 15 см). 
              Играют от 2 до 10 игроков (в официальных турнирах 2 или 4).
            </div>
            <div class="rulestext"> 
              У каждого игрока есть база (1 клетка), с которой он начинает ход. 
              Они располагаются в противоположных углах игрового поля. Клетки граничат как по сторонам, так и по диагонали.
            </div>

            <div class="stage"> Ход </div>
            <div class="rulestext">
              Каждый ход состоит из 3 действий. За одно действие можно или захватить пустую клетку поля, 
              или заразить чужую клетку. После заражения клетка уже никогда не может быть заражена повторно.
            </div>
            <div class="rulestext">
              Ходить можно либо рядом со своими живыми клетками, либо от зараженных Вами, 
              но при этом должна быть хотя бы одна Ваша живая клетка, граничащая с цепочкой зараженных Вами клеток.
            </div>

            <div class="stage"> Окончание </div>
            <div class="rulestext">
              Проигравшим считается тот, кто не может сделать ход. Происходит это вследствие того, 
              что все клетки вируса одного из игроков оказываются блокированы стенками из его клеток, заражённых соперником.
            </div>
          </slot>
        </section>

        <footer class="modal-footer">
          <slot name="footer">
            <button type="button"
                    class="btn-i-know"
                    @click="$emit('close')"
                    aria-label="Close modal"
            >
              Я все понял!
            </button>
          </slot>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
  export default {
    name: 'ModalRules',
  };
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: auto;
}
.modal {
  background: #005B8F;;
  box-shadow: 2px 2px 20px 1px;
  margin-top: 5vh;
  display: flex;
  width: 80%;
  flex-direction: column;
  max-width: 1000px;
}
.modal-header, .modal-footer {
  padding: 0.5vh;
  display: flex;
}
.modal-header {
  justify-content: space-between;
}
.head-text {
  flex: 25;
  font-size: 110%;
  margin-left: 3vh;
}
.modal-footer {
  justify-content: flex-end;
}
.modal-body {
  position: relative;
  padding:  1vh;
  font-size: 90%;
}
.btn-close {
  border: none;
  flex: 1;
  font-size: 130%;
  cursor: pointer;
  font-weight: bold;
  color: #4AAE9B;
  background: transparent;
}
.btn-i-know {
  text-align: center;
  border: 0px;
  margin: auto;
  background-color: #4AAE9B;
  color: white;
  font-family: Comic Sans MS, Comic Sans, cursive;
  width: 314px;
  height: 40px;
  -moz-border-radius: 157px / 20px;
  -webkit-border-radius: 157px /20px;
  border-radius: 157px /20px;
}
.stage {
  font-size: 130%;
  color: #00FFC2;
  padding-top: 0vh; 
}
@media (max-width: 650px) {
  .modal {
    margin-top: 50vh;
  }
}
</style>