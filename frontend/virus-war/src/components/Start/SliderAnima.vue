<template> 
  <div class="all">		
    <article id="slider">
      <input v-show='False' checked type="radio" name="slider" id="switch1">
      <input v-show='False' type="radio" name="slider" id="switch2">
      <input v-show='False' type="radio" name="slider" id="switch3">

      <div id="slides">
        <div id="overflow">
          <div class="image">
            <article><img src="../../assets/images/3.png"></article>
            <article><img src="../../assets/images/2.png"></article>
            <article><img src="../../assets/images/1.png"></article>

          </div>
        </div>
      </div>
      
      <div id="controls">
        <label for="switch1"></label>
        <label for="switch2"></label>
        <label for="switch3"></label>

      </div>
      
      <div id="active">
        <label for="switch1"></label>
        <label for="switch2"></label>
        <label for="switch3"></label>

      </div>
    </article>
  </div>
</template>

<script>
export default {
  name: "SliderAnima"
}
</script>

<style scoped>
.all {
  width: 75%;
}
#slider { /*положение слайдера*/
  position: relative;
  text-align: center;
  margin: 0 auto;
}

#slides {
  height:30%;
}
#slides article { /*все изображения справа друг от доруга*/
  width: 20%;
  float: left;
}
#slides .image { /*устанавливает общий размер блока с изображениями*/
  width: 500%;
  line-height: 0;
}
#overflow { /*сркывает все, что находится за пределами этого блока*/
  width: 100%;
  overflow: hidden;
}

article img { /*размер изображений слайдера*/
  width: 100%;
}

/*настройка переключения и положения для левой стрелки*/
/*если свич1-5 активны, то идет обращение к лейблу из блока с id контролс*/
#switch1:checked ~ #controls label:nth-child(5), 
#switch2:checked ~ #controls label:nth-child(1),
#switch3:checked ~ #controls label:nth-child(2),
#switch4:checked ~ #controls label:nth-child(3),
#switch5:checked ~ #controls label:nth-child(4) {
  background: url('../../assets/images/arrow_l.png') center/75% no-repeat; /*заливка фона картинкой без повторений*/
  float: left;
  margin: -25% 0 0 -45px; /*сдвиг влево*/
  display: block;
  height: 40px;
  width: 40px;
}

/*настройка переключения и положения для правой стрелки*/
#switch1:checked ~ #controls label:nth-child(2), 
#switch2:checked ~ #controls label:nth-child(3),
#switch3:checked ~ #controls label:nth-child(4),
#switch4:checked ~ #controls label:nth-child(5),
#switch5:checked ~ #controls label:nth-child(1) {
  background: url('../../assets/images/arrow_r.png') center/75% no-repeat; /*заливка фона картинкой без повторений next.png*/
  float: right;
  margin: -25% -40px 0 0; /*сдвиг вправо*/
  display: block;
  height: 40px;
  width:  40px;/*68px;*/
}

label, a {
  cursor: pointer;
}
#switch1:checked ~ #slides .image {
  margin-left: 0;
}
#switch2:checked ~ #slides .image {
  margin-left: -100%;
}
#switch3:checked ~ #slides .image {
  margin-left: -200%;
}
#switch4:checked ~ #slides .image {
  margin-left: -300%;
}
#switch5:checked ~ #slides .image {
  margin-left: -400%;
}

#controls { /*положение блока всех управляющих элементов*/
  margin: 0px 0 0 0;
  width: 100%;
  height: auto;
}
#active label { /*стиль отдельного переключателя*/
  border-radius: 10px; /*скругление углов*/
  display: inline-block; /*расположение в строку*/
  width: 15px;
  height: 15px;
  margin: 0 3px 0 3px;
  background: white;
}
#active { /*расположение блока с переключателями*/
  margin: 0px 0 0 0;
  text-align: center;
}
#active label:hover { /*поведение чекбокса при наведении*/
  background: #76c8ff;
  border-color: #777 !important; /*выполнение в любом случае*/
}

/*цвет активного лейбла при активации чекбокса*/
#switch1:checked ~ #active label:nth-child(1),
#switch2:checked ~ #active label:nth-child(2),
#switch3:checked ~ #active label:nth-child(3),
#switch4:checked ~ #active label:nth-child(4),
#switch5:checked ~ #active label:nth-child(5) {
  background: #18a3dd;
  border-color: #18a3dd !important;
}

#slides .image { /*анимация пролистывания изображений*/
  transition: all 800ms cubic-bezier(0.770, 0.000, 0.175, 1.000);
}
#controls label:hover { /*прозрачность стрелок при наведении*/
  opacity: 0.6;
}
#controls label { /*прозрачность стрелок при отводе курсора*/
  transition: opacity 0.2s ease-out;
}
</style>
