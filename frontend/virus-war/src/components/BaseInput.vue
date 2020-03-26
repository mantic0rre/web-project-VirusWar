<template>
  <input
    v-bind:value="value"
    v-on:input="$emit('input', $event.target.value)"
  >
</template>

<script>
export default {
  name: 'BaseInput',
  props: ['value'],
}
</script>

<style scoped>
input {
  background-color: white;
  text-align: center;
  border: 0px;
  border-radius: 100px 100px 0px 100px;
  margin: 0.2em auto;
  font-family: Comic Sans MS, Comic Sans, cursive;
  width: 75%;
  min-width: 200px;
  height:35px;
  outline: none;
}
</style>

